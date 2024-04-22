# Android

<!-- toc -->

- [Android Attributes](#android-attributes)
- [Deprecated Android Attributes](#deprecated-android-attributes)

<!-- tocstop -->

## Android Attributes

<!-- semconv registry.android(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `android.os.api_level` | string | Uniquely identifies the framework API revision offered by a version (`os.version`) of the android operating system. More information can be found [here](https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels). | `33`; `32` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->

## Deprecated Android Attributes

<!-- semconv registry.android.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `android.state` | string | Deprecated use the `device.app.lifecycle` event definition including `android.state` as a payload field instead. [1] | `created` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS identifiers` are derived.

`android.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->