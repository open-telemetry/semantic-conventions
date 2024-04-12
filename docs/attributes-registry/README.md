<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Registry
weight: -2
--->
# Attribute Registry

The attributes registry is the place where attributes are defined. An attribute definition covers the following properties of an attribute:

- the `id` (the fully qualified name) of the attribute
- the `type` of the attribute
- a `brief` description of the attribute and optionally a longer `note`
- example values

Attributes defined in the registry can be used in different semantic conventions. Attributes should be included in this registry before they are used in semantic conventions. Semantic conventions may override all the properties of an attribute except for the `id` and `type` in case it's required for a particular context. In addition, semantic conventions specify the requirement level of an attribute in the corresponding context.

A definition of an attribute in the registry doesn't necessarily imply that the attribute is used in any of the semantic conventions.

If applicable, application developers are encouraged to use existing attributes from this registry. See also [these recommendations][developers recommendations] regarding attribute selection and attribute naming for custom use cases.

All registered attributes are listed by namespace in this registry.

> **Warning**
> The following registry overview is a work in progress.
>
> Further attribute namespaces are currently being migrated and will appear in this registry soon.

Currently, the following namespaces exist:

* [android](android.md)
* [aws](aws.md)
* [browser](browser.md)
* [client](client.md)
* [cloud](cloud.md)
* [cloudevents](cloudevents.md)
* [code](code.md)
* [container](container.md)
* [db](db.md)
* [deployment](deployment.md)
* [destination](destination.md)
* [device](device.md)
* [disk](disk.md)
* [dns](dns.md)
* [enduser](enduser.md)
* [error](error.md)
* [event](event.md)
* [exception](exception.md)
* [faas](faas.md)
* [feature_flag](feature-flag.md)
* [file](file.md)
* [gcp](gcp.md)
* [graphql](graphql.md)
* [heroku](heroku.md)
* [host](host.md)
* [http](http.md)
* [ios](ios.md)
* [k8s](k8s.md)
* [messaging](messaging.md)
* [network](network.md)
* [oci](oci.md)
* [opentracing](opentracing.md)
* [os](os.md)
* [otel](otel.md)
* [peer](peer.md)
* [process](process.md)
* [rpc](rpc.md)
* [server](server.md)
* [service](service.md)
* [session](session.md)
* [source](source.md)
* [system](system.md)
* [telemetry](telemetry.md)
* [thread](thread.md)
* [tls](tls.md)
* [url](url.md)
* [user_agent](user-agent.md)
* [webengine](webengine.md)


[developers recommendations]: ../general/attribute-naming.md#recommendations-for-application-developers