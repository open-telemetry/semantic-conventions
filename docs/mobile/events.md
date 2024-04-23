# Semantic Conventions for mobile events

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for instrumentations that emit
events on mobile platforms. All mobile events MUST use a namespace of
`device` in the `event.name` property.

<!-- toc -->

- [Lifecycle instrumentation](#lifecycle-instrumentation)
  - [Event details](#event-details)

<!-- tocstop -->

## Lifecycle instrumentation

This section defines how to apply semantic conventions when instrumenting
application lifecycle. This event is meant to be used in conjunction with
`os.name` [resource semantic convention](/docs/resource/os.md) to identify the
mobile operating system (e.g. Android, iOS).

The following table describes the payload fields that MUST
be used to describe the state of the application at the time of the event.

The `android.state` and `ios.state` fields are mutually exclusive and MUST
NOT be used together, each field MUST be used with its corresponding
`os.name` [resource semantic convention](/docs/resource/os.md) value.

### Event details

<!-- semconv device.app.lifecycle(full) -->
The event name MUST be `device.app.lifecycle`.

<!-- endsemconv -->

<!-- Manually adding the markdown table until the body definition is available in the build tools -->
| Body Field | Type | Description  | Examples  | [Requirement Level](https://opentelemetry.io/docs/specs/semconv/general/attribute-requirement-level/) | Stability |
|---|---|---|---|---|---|
| `android.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [1] | `created` | `Conditionally Required`: if and only if `os.name` is `android` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `ios.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [2] | `active` | `Conditionally Required`: if and only if `os.name` is `ios` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS identifiers` are derived.

**[2]:** The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902), and from which the `OS terminology` column values are derived.

**Additional attribute requirements:** At least one of the following sets of attributes is required:

* `ios.state`
* `android.state`

`android.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

`ios.state` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `active` | The app has become `active`. Associated with UIKit notification `applicationDidBecomeActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `inactive` | The app is now `inactive`. Associated with UIKit notification `applicationWillResignActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | The app is now in the background. This value is associated with UIKit notification `applicationDidEnterBackground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | The app is now in the foreground. This value is associated with UIKit notification `applicationWillEnterForeground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- end of manually added table -->

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
