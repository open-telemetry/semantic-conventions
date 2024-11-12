# Blob Reference Properties

This refers to a way for attributes and fields to carry a reference to
data stored in an external storage system.

## Motivation

Much like with the usage of pointers in programming, there are use cases
where it is preferable to reference data rather than to copy it. There are
situations where it is impractical or inconvenient for a signal to include
the full value rather than to supply a reference; for example, the data may
be too large to fit within the limits of a signals operations backend. Or
there may be a situation in which the use of a reference is convenient for
applying a separate access control from that used for the signal data.

## In Open Telemetry Concepts

A blob reference property can exist in attributes (e.g. in spans, logs, span events)
as well as in event bodies. This document will use the term "reference attributes"
when referring to the use of Blob Reference Properties in attributes, while the
term "reference fields" will be used to refer to Blob Reference Properties in body fields.

## Minimal Requirement for a Blob Reference Property

The key `blob_ref.uri` or `{prefix}.blob_ref.uri` must exist and contain a valid URI. The
URI is presumed to refer to the storage location from which the referenced data may be retrieved.
The URI can be of any format, including HTTP ('http://'), HTTPS ('https://'), Google Cloud Storage ('gs://`),
Amazon S3 ('s3://'), Azure Blob ('azblob://'), or any other general or vendor-specific URI.

A key of the form `{prefix}.blob_ref.uri` indicates that the URI designates the location where the value
for the key named `{prefix}` has been stored. The prefix indicates a narrow scoping of the reference.

A key of the form `blob_ref.uri` with no prefix indicates that the containing object (such as the `AnyValue`
used to store the event body fields) in its entirety has its true value at the given location.

## Optional Metadata for Blob Reference Properties

A key of the form `{prefix}.blob_ref.uri` may be accompanied by `{prefix}.blob_ref.metadata-key` (and similarly `blob_ref.uri` may be accompanied by `blob_ref.metadata-key`) for certain, well-defined metadata.

The following metadata are defined and valid:

  - `[*.]blob_ref.content_type`: the MIME type of the data (e.g. `text/plain`, `application/json`, `application/octet-stream`)
  - `[*.]blob_ref.size`: the size of the attribute value in bytes
  - `[*.]blob_ref.hash_value`: a hash of the data for validation
  - `[*.]blob_ref.hash_algorithm`: the algorithm used to compute the hash

## Original Field/Key with a Reference

If both a Blob Reference Property and its non-reference variant appear together
within a signal (e.g. both `somekey` and `somekey.blob_ref.uri` are present),
it should be assumed that only the storage location specified by reference
contains the full, complete, original value of the data; the non-reference
variant may be used to preview/summarize the data but should be assumed to
potentially contain a truncated, redacted, or otherwise non-original value.
