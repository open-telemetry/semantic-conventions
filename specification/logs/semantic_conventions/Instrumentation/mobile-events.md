# Semantic Conventions for mobile instrumentation

**Status**: [Experimental][DocumentStatus]

This document defines semantic conventions for instrumentation on mobile platforms.

<!-- toc -->

- [Lifecycle instrumentation](#lifecycle-instrumentation)
  * [`state` values](#state-values)
    + [iOS](#ios)
    + [Android](#android)

<!-- tocstop -->

## Lifecycle instrumentation

This section defines how to apply semantic conventions when instrumenting application lifecycle.
This event is meant to be used in conjunction with `os.name` [resource semantic convention](https://github.com/open-telemetry/semantic-conventions/blob/main/specification/resource/semantic_conventions/os.md) to identify platform.

**Event name**: `client.lifecycle`

**Event domain**: `device`

The following attributes are stored in the `event.data` map.

| Attribute | Type   | Description                                | Examples          | Requirement level |
|-----------|--------|--------------------------------------------|-------------------|-------------------|
| `state`   | String | The state entered at the time of the event | platform specific | Required          |

### `state` values

#### iOS

The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902),
and from which the `OS terminology` column values are derived.

| Name         | OS terminology                 | description                               |
|--------------|--------------------------------|-------------------------------------------|
| `active`     | applicationDidBecomeActive     | The app has become "active"               |
| `inactive`   | applicationWillResignActive    | The app is about to become "inactive".    |
| `background` | applicationDidEnterBackground  | The app is now in the background.         |
| `foreground` | applicationWillEnterForeground | The app is about to enter the foreground. |
| `terminate`  | applicationWillTerminate       | The app is about to terminate.            |

#### Android

The Android lifecycle states are defined in [Activty lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS idenfifiers` are derived.

| Name         | OS terminology | description                                       |
|--------------|----------------|---------------------------------------------------|
| `created`    | [1]            | The app has been launched.                        |
| `foreground` | [2]            | The app is in the foreground or otherwise active. |
| `background` | [3]            | The app is in the background.                     |


[1] Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time
[2] Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states
[3] Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state
