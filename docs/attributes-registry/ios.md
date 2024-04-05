<!--- Hugo front matter used to generate the website version of this page:
--->

# iOS

<!-- toc -->

- [iOS Lifecycle Event Attributes](#ios-lifecycle-event-attributes)

<!-- tocstop -->

## iOS Lifecycle Event Attributes

<!-- semconv registry.ios.lifecycle.events(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `ios.state` | string | This attribute represents the state the application has transitioned into at the occurrence of the event. [1] | `active` | ![Experimental](https://img.shields.io/badge/-experimental-blue) |

**[1]:** The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902), and from which the `OS terminology` column values are derived.

`ios.state` MUST be one of the following:

| Value  | Description | Stability |
|---|---|---|
| `active` | The app has become `active`. Associated with UIKit notification `applicationDidBecomeActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `inactive` | The app is now `inactive`. Associated with UIKit notification `applicationWillResignActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | The app is now in the background. This value is associated with UIKit notification `applicationDidEnterBackground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | The app is now in the foreground. This value is associated with UIKit notification `applicationWillEnterForeground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
