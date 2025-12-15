# Contributing

Welcome to OpenTelemetry semantic conventions repository!

Before you start - see OpenTelemetry general
[contributing](https://github.com/open-telemetry/community/blob/main/guides/contributor/README.md)
requirements and recommendations.

<details>
<summary>Table of Contents</summary>

<!-- toc -->

- [Sign the CLA](#sign-the-cla)
- [How to contribute](#how-to-contribute)
  - [Which semantic conventions belong in this repo](#which-semantic-conventions-belong-in-this-repo)
  - [Suggesting conventions for a new area](#suggesting-conventions-for-a-new-area)
  - [Prerequisites](#prerequisites)
  - [1. Modify the YAML model](#1-modify-the-yaml-model)
    - [Code structure](#code-structure)
  - [2. Update the markdown files](#2-update-the-markdown-files)
    - [Hugo frontmatter](#hugo-frontmatter)
  - [3. Check new convention](#3-check-new-convention)
  - [4. Verify the changes before committing](#4-verify-the-changes-before-committing)
  - [5. Changelog](#5-changelog)
    - [When to add a changelog entry](#when-to-add-a-changelog-entry)
      - [Examples](#examples)
    - [Adding a changelog entry](#adding-a-changelog-entry)
  - [5. Getting your PR merged](#5-getting-your-pr-merged)
- [Reviewer guidelines](#reviewer-guidelines)
- [Automation](#automation)
  - [Consistency checks](#consistency-checks)
  - [Auto formatting](#auto-formatting)
  - [Markdown style](#markdown-style)
  - [Misspell check](#misspell-check)
  - [Update the tables of content](#update-the-tables-of-content)
  - [Markdown link check](#markdown-link-check)
  - [Yamllint check](#yamllint-check)
- [Schema files](#schema-files)
- [Merging existing ECS conventions](#merging-existing-ecs-conventions)

<!-- tocstop -->

</details>

## Sign the CLA

Before you can contribute, you will need to sign the [Contributor License
Agreement](https://identity.linuxfoundation.org/projects/cncf).

## How to contribute

When contributing to semantic conventions, it's important to understand a few
key, but non-obvious, aspects:

- In the PR description, include links to the relevant instrumentation and any applicable prototypes. Non-trivial changes to semantic conventions should be prototyped in the corresponding instrumentation(s).
- All attributes, metrics, etc. are formally defined in YAML files under
  the `model/` directory.
- All descriptions, normative language are defined in the `docs/` directory.
- All changes to existing attributes, metrics, etc. MUST be allowed as
  per our [stability guarantees][stability guarantees] and
  defined in a schema file.
- Links to the specification repository MUST point to a tag and **not** to the `main` branch.
  The tag version MUST match with the one defined in [README](README.md).

Please make sure all Pull Requests are compliant with these rules!

### Which semantic conventions belong in this repo

This repo contains semantic conventions supported by the OpenTelemetry ecosystem
including, but not limited to, components hosted in OpenTelemetry.

Instrumentations hosted in OpenTelemetry SHOULD contribute their semantic
conventions to this repo with the following exceptions:

- Instrumentations that follow external schema not fully compatible with OpenTelemetry such as
  [Kafka client JMX metrics](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/v2.10.0/instrumentation/kafka/kafka-clients/kafka-clients-2.6/library/README.md)
  or [RabbitMQ Collector Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.116.0/receiver/rabbitmqreceiver)
  SHOULD document such conventions in their own repository.

Having all OTel conventions in this repo allows to reuse common attributes, enforce naming and compatibility policies,
and helps to keep conventions consistent and backward compatible.

Want to define your own conventions outside this repo while building on OTel’s?
Come help us [decentralize semantic conventions](https://github.com/open-telemetry/weaver/issues/215).

### Suggesting conventions for a new area

Defining semantic conventions requires a group of people who are familiar with the domain,
are involved with instrumentation efforts, and are committed to be the point of contact for
pull requests, issues, and questions in this area.

Check out [project management](https://github.com/open-telemetry/community/blob/main/project-management.md)
for the details on how to start.

Refer to the [How to define new conventions](/docs/how-to-write-conventions/README.md)
document for guidance.

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

- If on MacOs, ensure you have `gsed` (GNU Sed) installed. If you have [HomeBrew](https://brew.sh)
  installed, then you can run the following command to install GSED.

  ```bash
  brew bundle
  ```

### 1. Modify the YAML model

Refer to the
[Semantic Convention YAML Language](https://github.com/open-telemetry/weaver/blob/main/schemas/semconv-syntax.md)
to learn how to make changes to the YAML files.

#### Code structure

The YAML (model definition) and Markdown (documentation) files are organized in the following way:

```
├── docs
│   ├── attribute_registry
│   ├── {root-namespace}
│   │   ├── README.md
│   │   ├── ....md
├── model
│   ├── {root-namespace}
│   │   ├── deprecated
│   │   |   ├── registry-deprecated.yaml
│   │   ├── events.yaml
│   │   ├── metrics.yaml
│   │   ├── registry.yaml
│   │   ├── resources.yaml
│   │   ├── spans.yaml
```

All attributes must be defined in the folder matching their root namespace under
`/model/{root-namespace}/registry.yaml` file.

Corresponding markdown files are auto-generated (see [Update the markdown files](#2-update-the-markdown-files))
in `/docs/attribute_registry` folder.

All semantic conventions definitions for telemetry signals should be placed under
`/model/{root-namespace}` and should follow `*{signal}.yaml` pattern. For example,
HTTP spans are defined in `model/http/spans.yaml`.

YAML definitions could be broken down into multiple files. For example, AWS spans
are defined in `/model/aws/lambda-spans.yaml` and `/model/aws/sdk-spans.yaml` files.

Deprecated conventions should be placed under `/model/{root-namespace}/deprecated`
folder.

### 2. Update the markdown files

After updating the YAML file(s), you need to update
the respective markdown files.
If you want to update existing tables, just run the following commands:

```bash
make table-generation registry-generation
```

When defining new telemetry signals (spans, metrics, events, resources) in YAML,
make sure to add a new markdown section describing them. Add the following
code-snippet into the markdown file:

```
<!-- semconv new-group-id -->
<!-- endsemconv -->
```

Then run markdown generation commands:

```bash
make table-generation registry-generation
```

#### Hugo frontmatter

At the top of all Markdown files under the `docs/` directory, you will see
headers like the following:

```md
<!--- Hugo front matter used to generate the website version of this page:
linkTitle: HTTP
--->
```

When creating new markdown files, you should provide the `linkTitle` attribute.
This is used to generate the navigation bar on the website,
and will be listed relative to the "parent" document.

### 3. Check new convention

Semantic conventions are validated for name formatting and backward compatibility with last released versions.
Here's [the full list of compatibility checks](./policies/compatibility.rego).

Removing attributes, metrics, or enum members is not allowed, they should be deprecated instead.
It applies to stable and unstable conventions and prevents semantic conventions auto-generated libraries from introducing breaking changes.

You can run backward compatibility check (along with other policies) in all yaml files with the following command:

```bash
make check-policies
```

### 4. Verify the changes before committing

Before sending a PR with your changes, make sure to run the automated checks:

```bash
make check
```

Alternatively, you can run each check individually.
Refer to the [Automation](#automation) section for more details.

### 5. Changelog

#### When to add a changelog entry

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

#### Adding a changelog entry

The [CHANGELOG.md](./CHANGELOG.md) files in this repo is autogenerated
from `.yaml` files in the [/.chloggen](/.chloggen) directory.

Your pull request should add a new `.yaml` file to this directory.
The name of your file can be arbitrary but must be unique since the last release.

During the release process, all `./.chloggen/*.yaml` files are transcribed into
`CHANGELOG.md` and then deleted.

1. Create an entry file using `make chlog-new`. The command generates a new file,
   with its name based on the current branch (e.g. `./.chloggen/my-feature-xyz.yaml`)
2. Fill in all the fields in the generated file
3. The value for the `component` field MUST match a folder name in the
   [model](https://github.com/open-telemetry/semantic-conventions/tree/main/model) directory
   (e.g. `browser`, `http`)
4. Run `make chlog-validate` to ensure the new file is valid
5. Commit and push the file

Alternately, copy `./.chloggen/TEMPLATE.yaml`, or just create your file from scratch.

### 5. Getting your PR merged

A PR (pull request) is considered to be **ready to merge** when:

- It has received at least two approvals from the [code owners](./.github/CODEOWNERS)
- There is no `request changes` from the [code owners](./.github/CODEOWNERS) for
  affected area(s)
- There is no open discussions
- It has been at least two working days since the last modification (except for
  the trivial updates, such like typo, cosmetic, rebase, etc.). This gives
  people reasonable time to review
- Trivial changes (typos, cosmetic changes, CI improvements, etc.) don't have to
  wait for two days

Any [maintainer](./README.md#contributing) can merge the PR once it is **ready
to merge**.

## Reviewer guidelines

Semantic conventions consist of multiple [areas](./AREAS.md) with ownership
defined in the [CODEOWNERS](./.github/CODEOWNERS) file.

When a PR is raised against specific area(s), it is recommended to allow the corresponding
area(s) owners to review and iterate on it first before approving or rejecting the PR.

A review from [@specs-semconv-approvers](https://github.com/orgs/open-telemetry/teams/specs-semconv-approvers)
is required on every PR and, in most cases, follows after area(s) owners approval.

Before merging a PR, [@specs-semconv-maintainers](https://github.com/orgs/open-telemetry/teams/specs-semconv-maintainers)
MUST verify that the PR has been approved by the corresponding area owner(s). For
non-trivial changes, maintainers SHOULD NOT merge PRs without other code owner approvals.

Reviews from non-code owners are encouraged, with the following assumptions:

- There is a reasonable intersection between the change and the reviewer's area of expertise or interest
- Area owners have autonomy to accept or dismiss feedback from non-codeowners and
  SHOULD consult with [@specs-semconv-maintainers](https://github.com/orgs/open-telemetry/teams/specs-semconv-maintainers)
  in case of conflicts

When reviewing changes, reviewers SHOULD include relevant context such as:

- Links to documentation related to the technology in question
- Links to applicable semantic conventions or OpenTelemetry guidelines
- Links to relevant PRs, issues, or discussions
- Reasons for suggesting the change

## Automation

Semantic Conventions provides a set of automated tools for general development.

### Consistency checks

The Specification has a number of tools it uses to check things like style,
spelling and link validity.

You can perform all checks locally using this command:

```bash
make check
```

> [!Note]
> `make check` can take a long time as it checks all links.
> You should use this prior to submitting a PR to ensure validity.
> However, you can run individual checks directly.

For more information on each check, see:

- [Markdown style](#markdown-style)
- [Misspell check](#misspell-check)
- [Markdown link check](#markdown-link-check)
- [Yamllint check](#yamllint-check)
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
- [Update the tables of content](#update-the-tables-of-content)
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

> [!Note]
> The `misspell` make target will also fetch and build the tool if
> necessary. You'll need [Go](https://go.dev) to build the spellchecker.

To quickly fix typos, use

```bash
make misspell-correction
```

### Update the tables of content

To update the tables of content, run:

```bash
make markdown-toc
```

### Markdown link check

To check the validity of links in all markdown files, run the following command:

```bash
make markdown-link-check
```

### Yamllint check

To check the validity of all yaml files, run the following command:

```bash
make yamllint
```

If it is the first time to run this command, install `yamllint` first:

```bash
make install-yamllint
```

## Schema files

> [!WARNING]
>
> DO NOT add your changes to files inside the `schemas` folder. These files are
> generated automatically by the release scripts and can't be updated after
> the corresponding version is released.

Release script uses the following command to generate new schema file:

```bash
make generate-schema-next NEXT_SEMCONV_VERSION={next version}
```

For details, please read
[the schema specification](https://opentelemetry.io/docs/specs/otel/schemas/).

## Merging existing ECS conventions

The Elastic Common Schema (ECS) is being merged into OpenTelemetry Semantic
Conventions per [OTEP 222][otep222]. When adding a semantic convention that
exists in some form in ECS, consider the following guidelines:

- Prefer using the existing ECS name when possible. In particular:
  - If proposing a name that differs from the ECS convention, provide usage
    data, user issue reports, feature requests, examples of prior work on a
    different standard or comparable evidence about the alternatives.
  - When no suitable alternatives are provided, altering an ECS name solely
    for the purpose of complying with [Name Pluralization guidelines](docs/general/naming.md#attribute-name-pluralization-guidelines)
    MAY BE avoided.
- Do not use an existing ECS name as a namespace. If the name must differ, use a
  different namespace name to avoid clashes or avoid using the namespace
  entirely. See the [ECS field reference] for existing namespaces.

[nvm]: https://github.com/nvm-sh/nvm/blob/master/README.md#installing-and-updating
[stability guarantees]: https://github.com/open-telemetry/opentelemetry-specification/blob/v1.37.0/specification/versioning-and-stability.md#semantic-conventions-stability
[otep222]: https://github.com/open-telemetry/oteps/pull/222
[ECS field reference]: https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html
