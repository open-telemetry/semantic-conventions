# Data Attributes - Usage and Examples

This document provides additional context and examples for the `data` attribute group.

## Overview

Traditional observability focuses on the health of the "vessel" (service, container, database). This specification introduces the Data Attribute Group, which focuses on the "cargo." By tagging resources and spans with data-specific metadata, we enable:

* **Automated Retention**: Systems can dynamically set snapshot lifetimes based on `data.category`.
* **Security Guardrails**: Monitoring for sensitive data movement across trust boundaries.
* **Compliance Mapping**: Real-time visibility into which services handle GDPR, HIPAA, or PCI-DSS governed data.

## Example Configurations

### 1. Kubernetes Resource Metadata

Infrastructure components like PersistentVolumeClaims (PVCs) act as the source of truth for the data sensitivity level.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: customer-data-pvc
  labels:
    # Defining the sensitivity of the "cargo" at rest
    data-classification: "restricted"
    data-category: "pii"
    compliance-scope: "gdpr"
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

### 2. OpenTelemetry Resource Attributes

When a service starts, it can be configured to broadcast its data handling capabilities or the sensitivity of its primary datastore via environment variables.

```bash
# Broadly tagging the service resource in the collection pipeline
export OTEL_RESOURCE_ATTRIBUTES="data.sensitivity=restricted,data.category=financial"
```

### 3. Programmatic Context Transfer (Pseudo-code)

To propagate sensitivity across a pipeline, a service injects the attribute into the Baggage, which is then carried in the headers of all downstream RPC calls.

```python
from opentelemetry import baggage, context

# 1. Extract sensitivity from the datastore metadata (e.g., K8s label)
store_sensitivity = "restricted"

# 2. Inject into the current request context as "Baggage"
ctx = baggage.set_baggage("data.sensitivity", store_sensitivity)

# 3. Downstream calls now carry this context automatically in their headers
with context.attach(ctx):
    # This RPC call to 'DownstreamService' will include the sensitivity attribute
    call_downstream_service()
```

## Security & Governance Considerations

1. **Low Cardinality**: To avoid performance degradation in metrics backends (like Prometheus), do not use unique IDs (e.g., `user_id`) in `data.*` attributes.
2. **No Actual Data**: Never place actual PII (e.g., an email address) inside these attributes. They are for metadata only.
