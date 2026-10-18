# Releasing

## Preparing a new release

- Close the [release milestone](https://github.com/open-telemetry/semantic-conventions/milestones)
  if there is one.
- Run [opentelemetry.io workflow](https://github.com/open-telemetry/opentelemetry.io/actions/workflows/build-dev.yml)
  against `semantic-conventions` submodule as a smoke-test for docs. Fix broken links, if any.
  - If there are failures you can't resolve, notify [#otel-comms](https://cloud-native.slack.com/archives/C02UN96HZH6)
    and corrdinate fixing them.
- Run the [prepare release workflow](https://github.com/open-telemetry/semantic-conventions/actions/workflows/prepare-release.yml).
  - Review and merge the pull request that it creates.
  - Note: the PR will need to be closed and the workflow re-run if any non-chore PRs are merged to `main` while the PR is open.

## Making the release

- Merging the prepare-release PR into `main` triggers the
  [create release draft workflow](.github/workflows/create-release.yml).
  It takes the version from the `otelbot/prepare-release-v{version}` branch and builds from the merge commit.
  It generates the resolved schema and attaches `resolved.yaml` and `manifest.yaml` to a draft release.
  - For manual runs, provide the release version and full commit SHA of the merged release PR.
- After the workflow succeeds, edit the draft in [releases](https://github.com/open-telemetry/semantic-conventions/releases):
  - Copy changelog to the release notes
    - Keep only the bottom sections under "New Contributors" from the generated release notes
  - Verify the release target, notes, and both schema assets
  - Publish release

New release is then auto-discovered by [opentelemetry.io](https://github.com/open-telemetry/opentelemetry.io) pipelines which (via bot-generated PR)
eventually results in new version of schema file being published.

## After the release

- Publishing a release triggers the [post-release workflow](https://github.com/open-telemetry/semantic-conventions/actions/workflows/post-release.yml),
  which opens a pull request against main bumping the development `schema_url` in
  `model/manifest.yaml` to the `{major}.{minor+1}.0-unreleased` version.
  Review and merge that pull request.
