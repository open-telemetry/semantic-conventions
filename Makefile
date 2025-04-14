# All documents to be used in spell check.
ALL_DOCS := $(shell find . -type f -name '*.md' -not -path './.github/*' -not -path './node_modules/*' | sort)
PWD := $(shell pwd)

# Determine OS & Arch for specific OS only tools on Unix based systems
OS := $(shell uname | tr '[:upper:]' '[:lower:]')
ifeq ($(OS),darwin)
	SED ?= gsed
else
	SED ?= sed
endif

TOOLS_DIR := $(PWD)/internal/tools

MARKDOWN_LINK_CHECK_ARG= # pass extra arguments such as --exclude '^http'
MISSPELL_BINARY=bin/misspell
MISSPELL = $(TOOLS_DIR)/$(MISSPELL_BINARY)

CHLOGGEN_BINARY=bin/chloggen
CHLOGGEN = $(TOOLS_DIR)/$(CHLOGGEN_BINARY)
CHLOGGEN_CONFIG  := .chloggen/config.yaml

# From where to resolve the containers (e.g. "otel/weaver").
CONTAINER_REPOSITORY=docker.io

# Per container overrides for the repository resolution.
WEAVER_CONTAINER_REPOSITORY=$(CONTAINER_REPOSITORY)
SEMCONVGEN_CONTAINER_REPOSITORY=$(CONTAINER_REPOSITORY)
OPA_CONTAINER_REPOSITORY=$(CONTAINER_REPOSITORY)

# Versioned, non-qualified references to containers used in this Makefile.
# These are parsed from dependencies.Dockerfile so dependabot will autoupdate
# the versions of docker files we use.
VERSIONED_WEAVER_CONTAINER_NO_REPO=$(shell cat dependencies.Dockerfile | awk '$$4=="weaver" {print $$2}')
VERSIONED_SEMCONVGEN_CONTAINER_NO_REPO=$(shell cat dependencies.Dockerfile | awk '$$4=="semconvgen" {print $$2}')
VERSIONED_OPA_CONTAINER_NO_REPO=$(shell cat dependencies.Dockerfile | awk '$$4=="opa" {print $$2}')

# Fully qualified references to containers used in this Makefile. These
# include the container repository, so that the build will work with tools
# like "podman" with a default "/etc/containers/registries.conf", where
# a default respository of "docker.io" is not assumed. This is intended to
# eliminate errors from podman such as:
#
#    Error: short-name "otel/weaver:v1.2.3" did not resolve to an alias
#    and no unqualified-search registries are defined in "/etc/containers/registries.conf"
WEAVER_CONTAINER=$(WEAVER_CONTAINER_REPOSITORY)/$(VERSIONED_WEAVER_CONTAINER_NO_REPO)
SEMCONVGEN_CONTAINER=$(SEMCONVGEN_CONTAINER_REPOSITORY)/$(VERSIONED_SEMCONVGEN_CONTAINER_NO_REPO)
OPA_CONTAINER=$(OPA_CONTAINER_REPOSITORY)/$(VERSIONED_OPA_CONTAINER_NO_REPO)


CHECK_TARGETS=install-tools markdownlint misspell table-check compatibility-check \
			schema-check check-file-and-folder-names-in-docs

# Determine if "docker" is actually podman
DOCKER_VERSION_OUTPUT := $(shell docker --version 2>&1)
DOCKER_IS_PODMAN := $(shell echo $(DOCKER_VERSION_OUTPUT) | grep -c podman)

ifeq ($(DOCKER_IS_PODMAN),0)
    DOCKER_COMMAND := docker
else
    DOCKER_COMMAND := podman
endif

# Debug printing
ifdef DEBUG
$(info Docker version output: $(DOCKER_VERSION_OUTPUT))
$(info Is Docker actually Podman? $(DOCKER_IS_PODMAN))
$(info Using command: $(DOCKER_COMMAND))
endif

DOCKER_RUN=$(DOCKER_COMMAND) run
DOCKER_USER=$(shell id -u):$(shell id -g)
DOCKER_USER_IS_HOST_USER_ARG=-u $(DOCKER_USER)
ifeq ($(DOCKER_COMMAND),podman)
 # On podman, additional arguments are needed to make "-u" work
 # correctly with the host user ID and host group ID.
 #
 #      Error: OCI runtime error: crun: setgroups: Invalid argument
 DOCKER_USER_IS_HOST_USER_ARG=--userns=keep-id -u $(DOCKER_USER)
endif


# TODO: add `yamllint` step to `all` after making sure it works on Mac.
.PHONY: all
all: $(CHECK_TARGETS) markdown-link-check

.PHONY: check
check: $(CHECK_TARGETS)

.PHONY: check-file-and-folder-names-in-docs
check-file-and-folder-names-in-docs:
	@found=`find docs -name '*_*'`; \
	if [ -n "$$found" ]; then \
		echo "Error: Underscores found in doc file or folder names, use hyphens instead:"; \
		echo $$found; \
		exit 1; \
	fi

$(MISSPELL):
	cd $(TOOLS_DIR) && go build -o $(MISSPELL_BINARY) github.com/client9/misspell/cmd/misspell

.PHONY: misspell
misspell:	$(MISSPELL)
	$(MISSPELL) -error $(ALL_DOCS)

.PHONY: misspell-correction
misspell-correction:	$(MISSPELL)
	$(MISSPELL) -w $(ALL_DOCS)

.PHONY: normalized-link-check
# NOTE: we check `model/[a-z]*` to avoid `model/README.md`, which contains
# valid occurrences of `../docs/`.
normalized-link-check:
	@if grep -R '\.\./docs/' docs model/[a-z]*; then \
		echo "\nERROR: Found occurrences of '../docs/'; see above."; \
		echo "       Remove the '../docs/' from doc page links referencing doc pages."; \
		exit 1; \
	else \
		echo "Normalized-link check passed."; \
	fi

.PHONY: markdown-link-check
markdown-link-check: normalized-link-check
	$(DOCKER_RUN) --rm \
		--mount 'type=bind,source=$(PWD),target=/home/repo' \
		lycheeverse/lychee \
		--config home/repo/.lychee.toml \
		--root-dir /home/repo \
		--verbose \
		$(MARKDOWN_LINK_CHECK_ARG) \
		home/repo

.PHONY: markdown-link-check-changelog-preview
markdown-link-check-changelog-preview:
	$(DOCKER_RUN) --rm \
		--mount 'type=bind,source=$(PWD),target=/home/repo' \
		lycheeverse/lychee \
		--config /home/repo/.lychee.toml \
		--root-dir /home/repo \
		--verbose \
		home/repo/changelog_preview.md

# This target runs markdown-toc on all files that contain
# a comment <!-- tocstop -->.
#
# The recommended way to prepare a .md file for markdown-toc is
# to add these comments:
#
#   <!-- toc -->
#   <!-- tocstop -->
.PHONY: markdown-toc
markdown-toc:
	@if ! npm ls markdown-toc; then npm install; fi
	@for f in $(ALL_DOCS); do \
		if grep -q '<!-- tocstop -->' $$f; then \
			echo markdown-toc: processing $$f; \
			npx --no -- markdown-toc --bullets "-" --no-first-h1 --no-stripHeadingTags -i $$f || exit 1; \
		elif grep -q '<!-- toc -->' $$f; then \
			echo markdown-toc: ERROR: '<!-- tocstop -->' missing from $$f; exit 1; \
		else \
			echo markdown-toc: no TOC markers, skipping $$f; \
		fi; \
	done

.PHONY: markdownlint
markdownlint:
	@if ! npm ls markdownlint-cli; then npm install; fi
	npx --no -- markdownlint-cli -c .markdownlint.yaml $(ALL_DOCS)

.PHONY: install-yamllint
install-yamllint:
    # Using a venv is recommended
	pip install -U yamllint~=1.26.1

.PHONY: yamllint
yamllint:
	yamllint .

# Generate markdown tables from YAML definitions
.PHONY: table-generation
table-generation:
	$(DOCKER_RUN) --rm \
		$(DOCKER_USER_IS_HOST_USER_ARG) \
		--mount 'type=bind,source=$(PWD)/templates,target=/home/weaver/templates,readonly' \
		--mount 'type=bind,source=$(PWD)/model,target=/home/weaver/source,readonly' \
		--mount 'type=bind,source=$(PWD)/docs,target=/home/weaver/target' \
		$(WEAVER_CONTAINER) registry update-markdown \
		--registry=/home/weaver/source \
		--attribute-registry-base-url=/docs/attributes-registry \
		--templates=/home/weaver/templates \
		--target=markdown \
		--future \
		/home/weaver/target

# Generate attribute registry markdown.
.PHONY: attribute-registry-generation
attribute-registry-generation:
	$(DOCKER_RUN) --rm \
		$(DOCKER_USER_IS_HOST_USER_ARG) \
		--mount 'type=bind,source=$(PWD)/templates,target=/home/weaver/templates,readonly' \
		--mount 'type=bind,source=$(PWD)/model,target=/home/weaver/source,readonly' \
		--mount 'type=bind,source=$(PWD)/docs,target=/home/weaver/target' \
		$(WEAVER_CONTAINER) registry generate \
		  --registry=/home/weaver/source \
		  --templates=/home/weaver/templates \
		  markdown \
		  /home/weaver/target/attributes-registry/

# Check if current markdown tables differ from the ones that would be generated from YAML definitions (weaver).
.PHONY: table-check
table-check:
	$(DOCKER_RUN) --rm \
		--mount 'type=bind,source=$(PWD)/templates,target=/home/weaver/templates,readonly' \
		--mount 'type=bind,source=$(PWD)/model,target=/home/weaver/source,readonly' \
		--mount 'type=bind,source=$(PWD)/docs,target=/home/weaver/target,readonly' \
		$(WEAVER_CONTAINER) registry update-markdown \
		--registry=/home/weaver/source \
		--attribute-registry-base-url=/docs/attributes-registry \
		--templates=/home/weaver/templates \
		--target=markdown \
		--dry-run \
		--future \
		/home/weaver/target

.PHONY: schema-check
schema-check:
	$(TOOLS_DIR)/schema_check.sh

# Run all checks in order of speed / likely failure.
# As a last thing, run attribute registry generation and git-diff for differences.
.PHONY: check
check: misspell markdownlint markdown-toc markdown-link-check check-policies attribute-registry-generation
	git diff --exit-code ':*.md' || (echo 'Generated markdown Table of Contents is out of date, please run "make markdown-toc" and commit the changes in this PR.' && exit 1)
	@echo "All checks complete"

# Attempt to fix issues / regenerate tables.
.PHONY: fix
fix: table-generation attribute-registry-generation misspell-correction markdown-toc
	@echo "All autofixes complete"

.PHONY: install-tools
install-tools: $(MISSPELL)
	npm install
	@echo "All tools installed"

$(CHLOGGEN):
	cd $(TOOLS_DIR) && go build -o $(CHLOGGEN_BINARY) go.opentelemetry.io/build-tools/chloggen

FILENAME?=$(shell git branch --show-current)
.PHONY: chlog-new
chlog-new: $(CHLOGGEN)
	$(CHLOGGEN) new --config $(CHLOGGEN_CONFIG) --filename $(FILENAME)

.PHONY: chlog-validate
chlog-validate: $(CHLOGGEN)
	$(CHLOGGEN) validate --config $(CHLOGGEN_CONFIG)

.PHONY: chlog-preview
chlog-preview: $(CHLOGGEN)
	$(CHLOGGEN) update --config $(CHLOGGEN_CONFIG) --dry

.PHONY: chlog-update
chlog-update: $(CHLOGGEN)
	$(CHLOGGEN) update --config $(CHLOGGEN_CONFIG) --version $(VERSION)

# Updates the areas (registry yaml file names) on all ISSUE_TEMPLATE
# files that have the "area" dropdown field
.PHONY: generate-gh-issue-templates
generate-gh-issue-templates:
	mkdir -p $(TOOLS_DIR)/bin
	$(DOCKER_RUN) --rm \
	$(DOCKER_USER_IS_HOST_USER_ARG) \
	--mount 'type=bind,source=$(PWD)/internal/tools/scripts,target=/home/weaver/templates,readonly' \
	--mount 'type=bind,source=$(PWD)/model,target=/home/weaver/source,readonly' \
	--mount 'type=bind,source=$(TOOLS_DIR)/bin,target=/home/weaver/target' \
	$(WEAVER_CONTAINER) registry generate \
		--registry=/home/weaver/source \
		--templates=/home/weaver/templates \
		--config=/home/weaver/templates/registry/areas-weaver.yaml \
		. \
		/home/weaver/target
	$(TOOLS_DIR)/scripts/update-issue-template-areas.sh $(PWD)/internal/tools/bin/areas.txt

# A previous iteration of calculating "LATEST_RELEASED_SEMCONV_VERSION"
# relied on "git describe". However, that approach does not work with
# light-weight developer forks/branches that haven't synced tags. Hence the
# more complex implementation of this using "git ls-remote".
#
# The output of "git ls-remote" looks something like this:
#
#    e531541025992b68177a68b87628c5dc75c4f7d9        refs/tags/v1.21.0
#    cadfe53949266d33476b15ca52c92f682600a29c        refs/tags/v1.22.0
#    ...
#
# .. which is why some additional processing is required to extract the
# latest version number and strip off the "v" prefix.
LATEST_RELEASED_SEMCONV_VERSION := $(shell git ls-remote --tags https://github.com/open-telemetry/semantic-conventions.git | cut -f 2 | sort --reverse | head -n 1 | tr '/' ' ' | cut -d ' ' -f 3 | $(SED) 's/v//g')
.PHONY: check-policies
check-policies:
	$(DOCKER_RUN) --rm \
		--mount 'type=bind,source=$(PWD)/policies,target=/home/weaver/policies,readonly' \
		--mount 'type=bind,source=$(PWD)/model,target=/home/weaver/source,readonly' \
		${WEAVER_CONTAINER} registry check \
		--registry=/home/weaver/source \
		--baseline-registry=https://github.com/open-telemetry/semantic-conventions/archive/refs/tags/v$(LATEST_RELEASED_SEMCONV_VERSION).zip[model] \
		--policy=/home/weaver/policies

# Test rego policies
.PHONY: test-policies
test-policies:
	$(DOCKER_RUN) --rm -v $(PWD)/policies:/policies -v $(PWD)/policies_test:/policies_test \
	${OPA_CONTAINER} test \
    --var-values \
	--explain fails \
	/policies \
	/policies_test

# TODO: This is now duplicative with weaver policy checks.  We can remove
# once github action requirements are updated.
.PHONY: compatibility-check
compatibility-check:
	$(DOCKER_RUN) --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec --pull=always \
		$(SEMCONVGEN_CONTAINER) --continue-on-validation-errors -f /source compatibility --previous-version $(LATEST_RELEASED_SEMCONV_VERSION)
