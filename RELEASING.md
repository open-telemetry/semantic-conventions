# Making a Release

- Ensure the referenced specification version is up to date. Use
  [tooling to update the spec](./CONTRIBUTING.md#updating-the-referenced-specification-version)
  if needed.
- Run [opentelemetry.io workflow](https://github.com/open-telemetry/opentelemetry.io/actions/workflows/build-dev.yml)
  against `semantic-conventions` submodule as a smoke-test for docs. Fix broken links, if any.
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
