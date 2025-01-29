# Releasing

## Preparing a new release

- Close the [release milestone](https://github.com/open-telemetry/semantic-conventions/milestones)
  if there is one.
- Run [opentelemetry.io workflow](https://github.com/open-telemetry/opentelemetry.io/actions/workflows/build-dev.yml)
  against `semantic-conventions` submodule as a smoke-test for docs. Fix broken links, if any.
- Run the [prepare release workflow](https://github.com/open-telemetry/semantic-conventions/actions/workflows/prepare-release.yml).
  - Review and merge the pull request that it creates.
  - Note: the PR will need to be closed and the workflow re-run if any non-chore PRs are merged to `main` while the PR is open.

## Making the release

- Create a [new release](https://github.com/open-telemetry/semantic-conventions/releases/new):
  - Set title and tag to `v{version}`
  - Set target to the commit of the merged release PR
  - Copy changelog to the release notes
    - First click the generate release notes button and keep only the bottom sections under "New Contributors"
  - Verify that the release looks like expected
  - Publish release

New release is then auto-discovered by [opentelemetry.io](https://github.com/open-telemetry/opentelemetry.io) pipelines which (via bot-generated PR)
eventually results in new version of schema file being published.
