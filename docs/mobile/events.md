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

<!-- semconv mobile-lifecycle-events -->
The event name MUST be `client.lifecycle`.

| Attribute  | Type | Description  | Examples  | Requirement Level |
|---|---|---|---|---|
| `event.data.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. | `created` | Required |

`event.data.state` MUST be one of the following:

| Value  | Description |
|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time. [1] |
| `active` | The app has become "active". Associated with UIKit notification `applicationDidBecomeActive`. [2] |
| `inactive` | the app is now "inactive". Associated with UIKit notification `applicationWillResignActive`. [2] |
| `background` | The app is now in the background. **On iOS**: this value is associated with UIKit notification `applicationDidEnterBackground`. **On Android:** Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state. |
| `foreground` | The app is now in the foreground. **On iOS:** this value is associated with UIKit notification `applicationWillEnterForeground`. **On Android:** Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. [2] |

**[1]:** Android only.

**[2]:** iOS only.
<!-- endsemconv -->

## iOS

The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902),
and from which the `OS terminology` column values are derived.

## Android

The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS idenfifiers` are derived.
