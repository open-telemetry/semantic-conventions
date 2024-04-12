
<!--- Hugo front matter used to generate the website version of this page:
--->

# ENDUSER

- [enduser](#enduser)


## enduser Attributes

| Attribute  | Type | Description  | Examples  | Stability |
|---|---|---|---|---|
| `enduser.id` | string | Username or client_id extracted from the access token or [Authorization](https://tools.ietf.org/html/rfc7235#section-4.2) header in the inbound request from outside the system.  |
username | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enduser.role` | string | Actual/assumed role the client is making the request under extracted from token or application security context.  |
admin | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
| `enduser.scope` | string | Scopes or granted authorities the client currently possesses extracted from token or application security context. The value would come from the scope associated with an [OAuth 2.0 Access Token](https://tools.ietf.org/html/rfc6749#section-3.3) or an attribute value in a [SAML 2.0 Assertion](http://docs.oasis-open.org/security/saml/Post2.0/sstc-saml-tech-overview-2.0.html).  |
read:message, write:files | ![Experimental](https://img.shields.io/badge/-experimental-blue) |
|---|---|---|---|---|


