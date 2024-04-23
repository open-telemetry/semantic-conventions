<!--- Hugo front matter used to generate the website version of this page:
--->

# iOS

<!-- toc -->

- [Deprecated iOS Attributes](#deprecated-ios-attributes)

<!-- tocstop -->

## Deprecated iOS Attributes

<!-- semconv registry.ios.deprecated(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `ios.state` | string | Deprecated use the `device.app.lifecycle` event definition including `ios.state` as a payload field instead. [1] | `active` | ![Deprecated](https://img.shields.io/badge/-deprecated-red)<br>Moved to a payload field of `device.app.lifecycle`. |

**[1]:** The iOS lifecycle states are defined in the [UIApplicationDelegate documentation](https://developer.apple.com/documentation/uikit/uiapplicationdelegate#1656902), and from which the `OS terminology` column values are derived.

`ios.state` has the following list of well-known values. If one of them applies, then the respective value MUST be used; otherwise, a custom value MAY be used.

| Value  | Description | Stability |
|---|---|---|
| `active` | The app has become `active`. Associated with UIKit notification `applicationDidBecomeActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `inactive` | The app is now `inactive`. Associated with UIKit notification `applicationWillResignActive`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `background` | The app is now in the background. This value is associated with UIKit notification `applicationDidEnterBackground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `foreground` | The app is now in the foreground. This value is associated with UIKit notification `applicationWillEnterForeground`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `terminate` | The app is about to terminate. Associated with UIKit notification `applicationWillTerminate`. | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
<!-- endsemconv -->
