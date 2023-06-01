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

**Event name**: `client.lifecycle`

**Event domain**: `device`

The following attributes are stored in the `event.data` map.

| Attribute        | Type   | Description                                | Examples          | Requirement level |
|------------------|--------|--------------------------------------------|-------------------|-------------------|
| `state` | String | The state entered at the time of the event | platform specific | Required          |

### `state` values

#### iOS

| Name                           | `state` Value | description                                |
|--------------------------------|------------------------|--------------------------------------------|
| applicationDidBecomeActive     | `active`               | The app has become "active"                |
| applicationWillResignActive    | `inactive`             | The app is about to become "inactive".     |
| applicationDidEnterBackground  | `background`           | The app is now in the background.          |
| applicationWillEnterForeground | `foreground`           | The app is about to enter the foreground.  |
| applicationWillTerminate       | `terminate`            | The app is about to terminate.             |

#### Android

| Name                 | `state` Value | description                                     |
|----------------------|------------------------|-------------------------------------------------|
| App process onCreate | `created`              | The app's process has been launched.            |
| App process onStart  | `started`              | The app is about to be shown in the foreground. |
| App process onResume | `resumed`              | The app is in the foreground.                   |
| App process onPause  | `paused`               | The app is about to go into the background.     |
| App process onStop   | `stopped`              | The app is in the background.                   |
