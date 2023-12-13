<!--- Hugo front matter used to generate the website version of this page:
linkTitle: Registry
weight: -2
--->

# Attributes Registry

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

* [Browser](browser.md)
* [Client](client.md)
* [Cloud](cloud.md)
* [Code](code.md)
* [Container](container.md)
* [DB](db.md) (database)
* [Destination](destination.md)
* [Device](device.md)
* [Disk](disk.md)
* [Error](error.md)
* [Host](host.md)
* [HTTP](http.md)
* [K8s](k8s.md)
* [Network](network.md)
* [OCI](oci.md)
* [OS](os.md)
* [Process](process.md)
* [RPC](rpc.md)
* [Server](server.md)
* [Source](source.md)
* [Thread](thread.md)
* [TLS](tls.md)
* [URL](url.md)
* [User agent](user-agent.md)

[developers recommendations]: ../general/attribute-naming.md#recommendations-for-application-developers
