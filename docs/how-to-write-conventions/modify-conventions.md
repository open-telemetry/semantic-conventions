<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Modify conventions
--->

# How to modify semantic conventions

For new conventions, see [How to write semantic conventions](README.md).

<!-- START doctoc -->

- [Describe the change](#describe-the-change)
- [Check compatibility](#check-compatibility)
- [Update the model and documentation](#update-the-model-and-documentation)
- [Validate and open the pull request](#validate-and-open-the-pull-request)
- [Respond to review](#respond-to-review)

<!-- END doctoc -->

## Describe the change

Search existing issues and pull requests first, then open a change proposal
issue. Include examples of the current and proposed telemetry.

Check the area's status and owners in [Semantic Convention Areas](/AREAS.md).
[Pull request triage](/issue-management.md#pull-request-triage) lists the issue
labels a pull request needs and the exceptions.

If triage asks for more information, add it to the issue. If the issue is
rejected, address the reason in the issue rather than opening a pull request.

## Check compatibility

Check each attribute, metric, or signal you change against the
[stability guarantees][stability]. Deprecate rather than remove, as described in
[Check new convention](/CONTRIBUTING.md#3-check-new-convention).

If users will need to migrate, describe in the issue how instrumentations and
consumers move from the old convention to the new one.

## Update the model and documentation

Change the YAML model and regenerate the Markdown as described in
[Contributing](/CONTRIBUTING.md#1-modify-the-yaml-model). Reuse existing
attributes where their meaning matches. Prototype non-trivial changes in the
relevant instrumentation (see [Prototyping](README.md#prototyping)).

Add a [changelog entry](/CONTRIBUTING.md#5-changelog) for user-facing changes.

## Validate and open the pull request

Run `make check` and fix what it reports. In the pull request, link the issue
and the prototype or instrumentation, and fill in the template.

## Respond to review

Answer questions with use cases or prototype results. If a change touches the
model, regenerate the Markdown and rerun `make check` before asking for another
review. The [merge requirements](/CONTRIBUTING.md#5-getting-your-pr-merged)
say when the pull request can merge.

If the pull request is closed, the review says why. Revise the proposal in the
issue, or stop there.

[stability]: https://opentelemetry.io/docs/specs/otel/versioning-and-stability/#semantic-conventions-stability
