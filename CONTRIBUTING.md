# Contributing

Welcome to OpenTelemetry semantic conventions repository!

Before you start - see OpenTelemetry general
[contributing](https://github.com/open-telemetry/community/blob/main/CONTRIBUTING.md)
requirements and recommendations.

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Sign the CLA](#sign-the-cla)
- [How to Contribute](#how-to-contribute)
  - [Prerequisites](#prerequisites)
  - [1. Modify the YAML model](#1-modify-the-yaml-model)
    - [Schema files](#schema-files)
  - [2. Update the markdown files](#2-update-the-markdown-files)
    - [Hugo frontmatter](#hugo-frontmatter)
  - [3. Verify the changes before committing](#3-verify-the-changes-before-committing)
  - [4. Changelog](#4-changelog)
    - [When to add a Changelog Entry](#when-to-add-a-changelog-entry)
      - [Examples](#examples)
    - [Adding a Changelog Entry](#adding-a-changelog-entry)
  - [5. Getting your PR merged](#5-getting-your-pr-merged)
- [Automation](#automation)
  - [Consistency Checks](#consistency-checks)
  - [Auto formatting](#auto-formatting)
  - [Markdown style](#markdown-style)
  - [Misspell check](#misspell-check)
  - [Markdown link check](#markdown-link-check)
  - [Version compatibility check](#version-compatibility-check)
- [Updating the referenced specification version](#updating-the-referenced-specification-version)
- [Making a Release](#making-a-release)
- [Merging existing ECS conventions](#merging-existing-ecs-conventions)

<!-- tocstop -->

</details>

## Sign the CLA

Before you can contribute, you will need to sign the [Contributor License
Agreement](https://identity.linuxfoundation.org/projects/cncf).

## How to Contribute

When contributing to semantic conventions, it's important to understand a few
key, but non-obvious, aspects:

- All attributes, metrics, etc. are formally defined in YAML files under
  the `model/` directory.
- All descriptions, normative language are defined in the `docs/` directory.
- All changes to existing attributes, metrics, etc. MUST be allowed as
  per our [stability guarantees][stability guarantees] and
  defined in a schema file. As part of any contribution, you should
  include attribute changes defined in the `schema-next.yaml` file.
- Links to the specification repository MUST point to a tag and **not** to the `main` branch.
  The tag version MUST match with the one defined in [README](README.md).

Please make sure all Pull Requests are compliant with these rules!

### Prerequisites

The Specification uses several tools to check things like style,
spelling and link validity. Before contributing, make sure to have your
environment configured:

- Install the latest LTS release of **[Node](https://nodejs.org/)**.
  For example, using **[nvm][]** under Linux run:

  ```bash
  nvm install --lts
  ```

- Then from the root of the project, install the tooling packages:

  ```bash
  npm install
  ```

### 1. Modify the YAML model

Refer to the
[Semantic Convention YAML Language](https://github.com/open-telemetry/build-tools/blob/v0.24.0/semantic-conventions/syntax.md)
to learn how to make changes to the YAML files.

#### Schema files

When making changes to existing semantic conventions (attributes, metrics, etc)
you MUST also update the `schema-next.yaml` file with the changes.

For details, please read
[the schema specification](https://opentelemetry.io/docs/specs/otel/schemas/).

You can also take examples from past changes inside the `schemas` folder.

> [!WARNING]
> DO NOT add your changes to files inside the `schemas` folder. Always add your
> changes to the `schema-next.yaml` file.

### 2. Update the markdown files

After updating the YAML file(s), you need to update
the respective markdown files. For this, run the following command:

```bash
make table-generation
```

#### Hugo frontmatter

At the top of all Markdown files under the `docs/` directory, you will see
headers like the following:

```md
<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP
path_base_for_github_subdir:
  from: content/en/docs/specs/semconv/http/_index.md
  to: http/README.md
--->
```

When creating new markdown files, you should provide the `linkTitle` attribute.
This is used to generate the navigation bar on the website,
and will be listed relative to the "parent" document.

### 3. Verify the changes before committing

Before sending a PR with your changes, make sure to run the automated checks:

```bash
make check
```

Alternatively, you can run each check individually.
Refer to the [Automation](#automation) section for more details.

### 4. Changelog

#### When to add a Changelog Entry

Pull requests that contain user-facing changes will require a changelog entry.
Keep in mind the following types of users (not limited to):

1. Those who are consuming the data following these conventions (e.g., in alerts, dashboards, queries)
2. Those who are using the conventions in instrumentations (e.g., library authors)
3. Those who are using the conventions to derive heuristics, predictions and automatic analyses (e.g., observability products/back-ends)

If a changelog entry is not required (e.g. editorial or trivial changes),
a maintainer or approver will add the `Skip Changelog` label to the pull request.

##### Examples

Changelog entry required:

- Any modification to existing conventions with change in functionality/behavior
- New semantic conventions
- Changes on definitions, normative language (in `/docs`)

No changelog entry:

- Typical documentation/editorial updates (e.g. grammar fixes, restructuring)
- Changes in internal tooling (e.g. make file, GH actions, etc)
- Refactorings with no meaningful change in functionality
- Chores, such as enabling linters, updating dependencies

#### Adding a Changelog Entry

The [CHANGELOG.md](./CHANGELOG.md) files in this repo is autogenerated
from `.yaml` files in the [/.chloggen](/.chloggen) directory.

Your pull request should add a new `.yaml` file to this directory.
The name of your file can be arbitrary but must be unique since the last release.

During the release process, all `./.chloggen/*.yaml` files are transcribed into
`CHANGELOG.md` and then deleted.

1. Create an entry file using `make chlog-new`. The command generates a new file,
   with its name based on the current branch (e.g. `./.chloggen/my-feature-xyz.yaml`)
2. Fill in all the fields in the generated file
3. The value for the `component` field MUST match a filename (without type) in the
   [registry](https://github.com/open-telemetry/semantic-conventions/tree/main/model/registry)
   (e.g. `browser`, `http`)
4. Run `make chlog-validate` to ensure the new file is valid
5. Commit and push the file

Alternately, copy `./.chloggen/TEMPLATE.yaml`, or just create your file from scratch.

### 5. Getting your PR merged

A PR (pull request) is considered to be **ready to merge** when:

- It has received at least two approvals from the [code
  owners](./.github/CODEOWNERS) (if approvals are from only one company, they
  won't count)
- There is no `request changes` from the [code owners](./.github/CODEOWNERS)
- There is no open discussions
- It has been at least two working days since the last modification (except for
  the trivial updates, such like typo, cosmetic, rebase, etc.). This gives
  people reasonable time to review
- Trivial changes (typos, cosmetic changes, CI improvements, etc.) don't have to
  wait for two days

Any [maintainer](./README.md#contributing) can merge the PR once it is **ready
to merge**.

## Automation

Semantic Conventions provides a set of automated tools for general development.

### Consistency Checks

The Specification has a number of tools it uses to check things like style,
spelling and link validity.

You can perform all checks locally using this command:

```bash
make check
```

> Note: `make check` can take a long time as it checks all links.
> You should use this prior to submitting a PR to ensure validity.
> However, you can run individual checks directly.

For more information on each check, see:

- [Markdown style](#markdown-style)
- [Misspell check](#misspell-check)
- [Markdown link check](#markdown-link-check)
- Prettier formatting

### Auto formatting

Semantic conventions have some autogenerated components and additionally can do
automatic style/spell correction. You can run all of this via:

```bash
make fix
```

You can also run these fixes individually.

See:

- [Misspell Correction](#misspell-check)
- [Update the markdown files](#2-update-the-markdown-files)

### Markdown style

Markdown files should be properly formatted before a pull request is sent out.
In this repository we follow the
[markdownlint rules](https://github.com/DavidAnson/markdownlint#rules--aliases)
with some customizations. See [markdownlint](.markdownlint.yaml) or
[settings](.vscode/settings.json) for details.

We highly encourage to use line breaks in markdown files at `80` characters
wide. There are tools that can do it for you effectively. Please submit proposal
to include your editor settings required to enable this behavior so the out of
the box settings for this repository will be consistent.

To check for style violations, run:

```bash
make markdownlint
```

To fix style violations, follow the
[instruction](https://github.com/DavidAnson/markdownlint#optionsresultversion)
with the Node version of markdownlint. If you are using Visual Studio Code,
you can also use the `fixAll` command of the
[vscode markdownlint extension](https://github.com/DavidAnson/vscode-markdownlint).

### Misspell check

In addition, please make sure to clean up typos before you submit the change.

To check for typos, run the following command:

```bash
make misspell
```

> **NOTE**: The `misspell` make target will also fetch and build the tool if
> necessary. You'll need [Go](https://go.dev) to build the spellchecker.

To quickly fix typos, use

```bash
make misspell-correction
```

### Markdown link check

To check the validity of links in all markdown files, run the following command:

```bash
make markdown-link-check
```

### Version compatibility check

Semantic conventions are validated for backward compatibility with last released versions. Here's [the full list of compatibility checks](https://github.com/open-telemetry/build-tools/blob/main/semantic-conventions/README.md#version-compatibility-check).
Removing attributes, metrics, or enum members is not allowed, they should be deprecated instead.
It applies to stable and experimental conventions and prevents semantic conventions auto-generated libraries from introducing breaking changes.

You can run backward compatibility check in all yaml files with the following command:

```bash
make compatibility-check
```

## Updating the referenced specification version

1. Open the `./internal/tools/update_specification_version.sh` script.
2. Modify the `PREVIOUS_SPECIFICATION_VERSION` to be the same value as `LATEST_SPECIFICATION_VERSION`
3. Modify `LATEST_SPECIFICATION_VERSION` to the latest specification tag, e.g. `1.21`
4. Run the script from the root directory, e.g. `semantic-conventions$ ./internal/tools/update_specification_version.sh`.
5. Add all modified files to the change submit and submit a PR.

## Making a Release

- Ensure the referenced specification version is up to date. Use
  [tooling to update the spec](#updating-the-referenced-specification-version)
  if needed.
- Create a staging branch for the release.
  - Update `schema-next.yaml` file and move to `schemas/{version}`
    - Ensure the `next` version is appropriately configured as the `{version}`.
    - Copy `schema-next.yaml` to `schemas/{version}`.
    - Add `next` as a version in `schema-next.yaml` version.
  - Run `make chlog-update VERSION=v{version}`
    - `make chlog-update` will clean up all the current `.yaml` files inside the
      `.chloggen` folder automatically
    - Double check that `CHANGELOG.md` is updated with the proper `v{version}`
  - Send staging branch as PR for review.
- After the release PR is merged, create a [new release](https://github.com/open-telemetry/semantic-conventions/releases/new):
  - Set title and tag to `v{version}`
  - Set target to the commit of the merged release PR
  - Copy changelog to the release notes
  - Verify that the release looks like expected
  - Publish release

New release is then auto-discovered by [opentelemetry.io](https://github.com/open-telemetry/opentelemetry.io) pipelines which (via bot-generated PR)
eventually results in new version of schema file being published.

## Merging existing ECS conventions

The Elastic Common Schema (ECS) is being merged into OpenTelemetry Semantic
Conventions per [OTEP 222][otep222]. When adding a semantic convention that
exists in some form in ECS, consider the following guidelines:

- Prefer using the existing ECS name when possible. In particular:
  - If proposing a name that differs from the ECS convention, provide usage
    data, user issue reports, feature requests, examples of prior work on a
    different standard or comparable evidence about the alternatives.
  - When no suitable alternatives are provided, altering an ECS name solely
    for the purpose of complying with [Name Pluralization guidelines](docs/general/attribute-naming.md#name-pluralization-guidelines)
    MAY BE avoided.
- Do not use an existing ECS name as a namespace. If the name must differ, use a
  different namespace name to avoid clashes or avoid using the namespace
  entirely. See the [ECS field reference] for existing namespaces.

[nvm]: https://github.com/nvm-sh/nvm/blob/master/README.md#installing-and-updating
[stability guarantees]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/versioning-and-stability.md#semantic-conventions-stability
[otep222]: https://github.com/open-telemetry/oteps/pull/222
[ECS field reference]: https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html
