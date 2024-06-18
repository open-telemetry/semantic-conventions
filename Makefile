# All documents to be used in spell check.
ALL_DOCS := $(shell find . -type f -name '*.md' -not -path './.github/*' -not -path './node_modules/*' | sort)
PWD := $(shell pwd)

TOOLS_DIR := ./internal/tools

MISSPELL_BINARY=bin/misspell
MISSPELL = $(TOOLS_DIR)/$(MISSPELL_BINARY)

CHLOGGEN_BINARY=bin/chloggen
CHLOGGEN = $(TOOLS_DIR)/$(CHLOGGEN_BINARY)
CHLOGGEN_CONFIG  := .chloggen/config.yaml

# see https://github.com/open-telemetry/build-tools/releases for semconvgen updates
# Keep links in model/README.md and .vscode/settings.json in sync!
SEMCONVGEN_VERSION=0.24.0
WEAVER_VERSION=0.4.0

# From where to resolve the containers (e.g. "otel/weaver").
CONTAINER_REPOSITORY=docker.io

# Per container overrides for the repository resolution.
WEAVER_CONTAINER_REPOSITORY=$(CONTAINER_REPOSITORY)
SEMCONVGEN_CONTAINER_REPOSITORY=$(CONTAINER_REPOSITORY)

# Fully qualified references to containers used in this Makefile.
WEAVER_CONTAINER=$(WEAVER_CONTAINER_REPOSITORY)/otel/weaver:$(WEAVER_VERSION)
SEMCONVGEN_CONTAINER=$(SEMCONVGEN_CONTAINER_REPOSITORY)/otel/semconvgen:$(SEMCONVGEN_VERSION)

# TODO: add `yamllint` step to `all` after making sure it works on Mac.
.PHONY: all
all: install-tools markdownlint markdown-link-check misspell table-check compatibility-check schema-check \
		 check-file-and-folder-names-in-docs

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

.PHONY: markdown-link-check
markdown-link-check:
	@if ! npm ls markdown-link-check; then npm install; fi
	@for f in $(ALL_DOCS); do \
		npx --no -- markdown-link-check --quiet --config .markdown_link_check_config.json $$f \
			|| exit 1; \
	done

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
		else \
			echo markdown-toc: no TOC markers, skipping $$f; \
		fi; \
	done

.PHONY: markdownlint
markdownlint:
	@if ! npm ls markdownlint; then npm install; fi
	@npx gulp lint-md

.PHONY: markdownlint-old
markdownlint-old:
	@if ! npm ls markdownlint; then npm install; fi
	@for f in $(ALL_DOCS); do \
		echo $$f; \
		npx --no -p markdownlint-cli markdownlint -c .markdownlint.yaml $$f \
			|| exit 1; \
	done

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
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec -v $(PWD)/templates:/weaver/templates \
		$(WEAVER_CONTAINER) registry update-markdown \
		--registry=/source \
		--attribute-registry-base-url=/docs/attributes-registry \
		--templates=/weaver/templates \
		--target=markdown \
		/spec

# Generate attribute registry markdown.
.PHONY: attribute-registry-generation
attribute-registry-generation:
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec -v $(PWD)/templates:/weaver/templates \
		$(WEAVER_CONTAINER) registry generate \
		  --registry=/source \
		  --templates=/weaver/templates \
		  markdown \
		  /spec/attributes-registry/
	npm run fix:format

# Check if current markdown tables differ from the ones that would be generated from YAML definitions (weaver).
.PHONY: table-check
table-check:
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec -v $(PWD)/templates:/weaver/templates \
		$(WEAVER_CONTAINER) registry update-markdown \
		--registry=/source \
		--attribute-registry-base-url=/docs/attributes-registry \
		--templates=/weaver/templates \
		--target=markdown \
		--dry-run \
		/spec


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
LATEST_RELEASED_SEMCONV_VERSION := $(shell git ls-remote --tags https://github.com/open-telemetry/semantic-conventions.git | cut -f 2 | sort --reverse | head -n 1 | tr '/' ' ' | cut -d ' ' -f 3 | sed 's/v//g')
.PHONY: compatibility-check
compatibility-check:
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec --pull=always \
		$(SEMCONVGEN_CONTAINER) -f /source compatibility --previous-version $(LATEST_RELEASED_SEMCONV_VERSION)

.PHONY: schema-check
schema-check:
	$(TOOLS_DIR)/schema_check.sh

.PHONY: check-format
check-format:
	npm run check:format

.PHONY: fix-format
fix-format:
	npm run fix:format

# Run all checks in order of speed / likely failure.
# As a last thing, run attribute registry generation and git-diff for differences.
.PHONY: check
check: misspell markdownlint check-format markdown-toc compatibility-check markdown-link-check attribute-registry-generation
	git diff --exit-code ':*.md' || (echo 'Generated markdown Table of Contents is out of date, please run "make markdown-toc" and commit the changes in this PR.' && exit 1)
	@echo "All checks complete"

# Attempt to fix issues / regenerate tables.
.PHONY: fix
fix: table-generation attribute-registry-generation misspell-correction fix-format markdown-toc
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
	$(TOOLS_DIR)/scripts/update-issue-template-areas.sh

#.PHONY: codegen-collision-checks
codegen-collision-checks:
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/:/output \
		$(WEAVER_CONTAINER) registry resolve \
		--registry=/source \
		--output=/output/resolved.json \
		-f json;
	$(PWD)/node_modules/node-jq/bin/jq.exe -f $(TOOLS_DIR)/codegen_collisions_check.jq ./resolved.json