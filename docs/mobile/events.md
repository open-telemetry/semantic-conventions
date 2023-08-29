# Semantic Conventions for mobile instrumentation

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for instrumentation on mobile platforms.

<!-- toc -->

- [Lifecycle instrumentation](#lifecycle-instrumentation)
- [iOS](#ios)
- [Android](#android)

<!-- tocstop -->

## Lifecycle instrumentation

This section defines how to apply semantic conventions when instrumenting application lifecycle.
This event is meant to be used in conjunction with `os.name` [resource semantic convention](/docs/resource/os.md) to identify platform.

<!-- semconv ios-lifecycle-events -->
The event name MUST be `app.lifecycle`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `ios.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. | `active` | Required |

`ios.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `active` | The app has become "active". Associated with UIKit notification `applicationDidBecomeActive`. |
| `inactive` | the app is now "inactive". Associated with UIKit notification `applicationWillResignActive`. |
| `background` | The app is now in the background. This value is associated with UIKit notification `applicationDidEnterBackground`. |
| `foreground` | The app is now in the foreground. this value is associated with UIKit notification `applicationWillEnterForeground`. |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. |
<!-- endsemconv -->

<!-- semconv android-lifecycle-events -->
The event name MUST be `app.lifecycle`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `android.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. | `created` | Required |

`android.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService()  has been called in the app for the first time.' |
| `background` | Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state. |
| `foreground` | Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states. |
<!-- endsemconv -->

## iOS

The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902),
and from which the `OS terminology` column values are derived.

## Android

The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS idenfifiers` are derived.

[DocumentStatus]: https://github.com/open-telemetry/opentelemetry-specification/tree/v1.22.0/specification/document-status.md
