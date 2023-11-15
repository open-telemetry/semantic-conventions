<!--- Hugo front matter used to generate the website version of this page:
--->

# Device

## Device Attributes

<!-- semconv registry.device(omit_requirement_level) -->
| Attribute  | Type | Description  | Examples  |
|---|---|---|---|
| `device.id` | string | A unique identifier representing the device [1] | `2ab2916d-a51f-4ac8-80ee-45ac31a28092` |
| `device.manufacturer` | string | The name of the device manufacturer [2] | `Apple`; `Samsung` |
| `device.model.identifier` | string | The model identifier for the device [3] | `iPhone3,4`; `SM-G920F` |
| `device.model.name` | string | The marketing name for the device model [4] | `iPhone 6s Plus`; `Samsung Galaxy S6` |

**[1]:** The device identifier MUST only be defined using the values outlined below. This value is not an advertising identifier and MUST NOT be used as such. On iOS (Swift or Objective-C), this value MUST be equal to the [vendor identifier](https://developer.apple.com/documentation/uikit/uidevice/1620059-identifierforvendor). On Android (Java or Kotlin), this value MUST be equal to the Firebase Installation ID or a globally unique UUID which is persisted across sessions in your application. More information can be found [here](https://developer.android.com/training/articles/user-data-ids) on best practices and exact implementation details. Caution should be taken when storing personal data or anything which can identify a user. GDPR and data protection laws may apply, ensure you do your own due diligence.

**[2]:** The Android OS provides this field via [Build](https://developer.android.com/reference/android/os/Build#MANUFACTURER). iOS apps SHOULD hardcode the value `Apple`.

**[3]:** It's recommended this value represents a machine-readable version of the model identifier rather than the market or consumer-friendly name of the device.

**[4]:** It's recommended this value represents a human-readable version of the device model rather than a machine-readable alternative.
<!-- endsemconv -->
