
<!--- Hugo front matter used to generate the website version of this page:
--->

# ANDROID

- [android](#android)
- [android lifecycle events](#android lifecycle events)
- [Notes](#notes)

## android Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `android.os.api_level` | string | Uniquely identifies the framework API revision offered by a version (`os.version`) of the android operating system. More information can be found [here](https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels).  |`33`; `32` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|


## android lifecycle events Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `android.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [1] |`created`; `background`; `foreground` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|

`android.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `created` | Any time before Activity.onResume() or, if the app has no Activity, Context.startService() has been called in the app for the first time.
 |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | Any time after Activity.onPause() or, if the app has no Activity, Context.stopService() has been called when the app was in the foreground state.
 |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | Any time after Activity.onResume() or, if the app has no Activity, Context.startService() has been called when the app was in either the created or background states.
 |  ![Experimental](https://img.shields.io/badge/-experimental-blue) |

## Notes

[1]: The Android lifecycle states are defined in [Activity lifecycle callbacks](https://developer.android.com/guide/components/activities/activity-lifecycle#lc), and from which the `OS identifiers` are derived.

