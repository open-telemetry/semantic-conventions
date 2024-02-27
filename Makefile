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
SEMCONVGEN_VERSION=0.23.0

# TODO: add `yamllint` step to `all` after making sure it works on Mac.
.PHONY: all
all: install-tools markdownlint markdown-link-check misspell table-check schema-check \
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
# The recommended way to prepate a .md file for markdown-toc is
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
			npx --no -- markdown-toc --no-first-h1 --no-stripHeadingTags -i $$f || exit 1; \
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
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec \
		otel/semconvgen:$(SEMCONVGEN_VERSION) -f /source markdown -md /spec --md-use-badges --md-stable

# Check if current markdown tables differ from the ones that would be generated from YAML definitions
.PHONY: table-check
table-check:
	docker run --rm -v $(PWD)/model:/source -v $(PWD)/docs:/spec \
		otel/semconvgen:$(SEMCONVGEN_VERSION) -f /source markdown -md /spec --md-check --md-use-badges --md-stable

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
.PHONY: check
check: misspell markdownlint markdown-link-check check-format
	@echo "All checks complete"

# Attempt to fix issues / regenerate tables.
.PHONY: fix
fix: table-generation misspell-correction fix-format
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
