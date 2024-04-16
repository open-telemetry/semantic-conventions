# Heroku

**Status**: [Experimental][DocumentStatus]

**type:** `heroku`

**Description:** [Heroku dyno metadata]

<!-- semconv heroku -->
| Attribute  | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| [`heroku.app.id`](../../attributes-registry/heroku.md) | string | Unique identifier for the application | `2daa2797-e42b-4624-9322-ec3f968df4da` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`heroku.release.commit`](../../attributes-registry/heroku.md) | string | Commit hash for the current release | `e6134959463efd8966b20e75b913cafe3f5ec` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| [`heroku.release.creation_timestamp`](../../attributes-registry/heroku.md) | string | Time and date the release was created | `2022-10-23T18:00:42Z` | `Opt-In` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

**Mapping:**

| Dyno metadata environment variable | Resource attribute                  |
|------------------------------------|-------------------------------------|
| `HEROKU_APP_ID`                    | `heroku.app.id`                     |
| `HEROKU_APP_NAME`                  | `service.name`                      |
| `HEROKU_DYNO_ID`                   | `service.instance.id`               |
| `HEROKU_RELEASE_CREATED_AT`        | `heroku.release.creation_timestamp` |
| `HEROKU_RELEASE_VERSION`           | `service.version`                   |
| `HEROKU_SLUG_COMMIT`               | `heroku.release.commit`             |

Additionally, [the `cloud.provider` resource attribute MUST be set to `heroku`](../cloud.md).

[Heroku dyno metadata]: https://devcenter.heroku.com/articles/dyno-metadata

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.31.0/specification/document-status.md
