"""
GenAI Memory Semantic Conventions - Exporter Setup Utilities

This module provides utilities for setting up OpenTelemetry exporters
for GenAI Memory operations tracing.

Supported exporters:
- Console: Simple output for development and debugging
- OTLP: Standard OpenTelemetry Protocol for production backends
- Jaeger: Direct Jaeger exporter (legacy, prefer OTLP)
- App Insights: Azure Monitor exporter (connection string)
- Laminar: OTLP gRPC exporter with bearer auth
- Langfuse: OTLP HTTP exporter with basic auth
- Traceloop: Traceloop SDK (sets up its own provider)

Example usage:
    from genai_memory_otel import setup_tracing

    # Simple console output
    tracer = setup_tracing(service_name="my-agent")

    # With OTLP backend
    tracer = setup_tracing(
        service_name="my-agent",
        use_console=False,
        use_otlp=True,
        otlp_endpoint="http://localhost:4317",
    )
"""

import atexit
import base64
import os
from typing import List, Optional

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


def _parse_exporters(value: str) -> List[str]:
    return [part.strip().lower() for part in value.split(",") if part.strip()]


def _get_azure_exporter():
    """Configure Azure Application Insights exporter."""
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not connection_string:
        print("[SKIP] App Insights: APPLICATIONINSIGHTS_CONNECTION_STRING not set")
        return None

    try:
        from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

        exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        print("[OK] App Insights: configured")
        return exporter
    except ImportError as e:
        print("[SKIP] App Insights: azure-monitor-opentelemetry-exporter not installed or incompatible")
        print(f"       Error: {e}")
        return None
    except Exception as e:
        print(f"[SKIP] App Insights: failed to configure - {e}")
        return None


def _get_laminar_exporter():
    """Configure Laminar OTLP exporter."""
    api_key = os.environ.get("LMNR_PROJECT_API_KEY")
    if not api_key:
        print("[SKIP] Laminar: LMNR_PROJECT_API_KEY not set")
        return None

    try:
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

        exporter = OTLPSpanExporter(
            endpoint="https://api.lmnr.ai:8443",
            headers={"authorization": f"Bearer {api_key}"},
        )
        print("[OK] Laminar: configured (api.lmnr.ai:8443)")
        return exporter
    except ImportError as e:
        print("[SKIP] Laminar: opentelemetry-exporter-otlp-proto-grpc not installed or incompatible")
        print(f"       Error: {e}")
        return None
    except Exception as e:
        print(f"[SKIP] Laminar: failed to configure - {e}")
        return None


def _get_langfuse_exporter():
    """Configure Langfuse OTLP HTTP exporter with Basic Auth."""
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    base_url = os.environ.get("LANGFUSE_BASE_URL", "https://us.cloud.langfuse.com")

    if not public_key or not secret_key:
        print("[SKIP] Langfuse: LANGFUSE_PUBLIC_KEY and/or LANGFUSE_SECRET_KEY not set")
        return None

    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        auth_string = f"{public_key}:{secret_key}"
        auth_b64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
        endpoint = f"{base_url}/api/public/otel/v1/traces"

        exporter = OTLPSpanExporter(
            endpoint=endpoint,
            headers={"Authorization": f"Basic {auth_b64}"},
        )
        print(f"[OK] Langfuse: configured ({base_url})")
        return exporter
    except ImportError as e:
        print("[SKIP] Langfuse: opentelemetry-exporter-otlp-proto-http not installed or incompatible")
        print(f"       Error: {e}")
        return None
    except Exception as e:
        print(f"[SKIP] Langfuse: failed to configure - {e}")
        return None


def _configure_traceloop(
    *,
    service_name: str,
    service_version: str,
    capture_content: bool,
    disable_batch: bool,
):
    """Configure Traceloop SDK (handles its own tracer provider + exporter setup)."""
    api_key = os.environ.get("TRACELOOP_API_KEY")
    if not api_key:
        print("[SKIP] Traceloop: TRACELOOP_API_KEY not set")
        return None

    try:
        from traceloop.sdk import Traceloop

        Traceloop.init(
            app_name=service_name,
            disable_batch=disable_batch,
            api_key=api_key,
            resource_attributes={
                SERVICE_NAME: service_name,
                SERVICE_VERSION: service_version,
                "genai.memory.capture_content": str(capture_content).lower(),
            },
        )
        print("[OK] Traceloop: SDK initialized")
        return trace.get_tracer_provider()
    except ImportError as e:
        print("[SKIP] Traceloop: traceloop-sdk not installed or incompatible")
        print(f"       Error: {e}")
        return None
    except Exception as e:
        print(f"[SKIP] Traceloop: failed to configure - {e}")
        return None


def setup_tracing(
    service_name: str = "genai-memory-prototype",
    service_version: str = "0.1.0",
    *,
    use_console: bool = True,
    use_otlp: bool = False,
    otlp_endpoint: Optional[str] = None,
    use_jaeger: bool = False,
    jaeger_endpoint: Optional[str] = None,
    capture_content: bool = False,
    exporters: Optional[List[str]] = None,
    use_simple_processor: bool = False,
) -> trace.Tracer:
    """
    Set up OpenTelemetry tracing with configurable exporters.

    This function initializes the OpenTelemetry tracing infrastructure
    with the specified exporters and returns a tracer ready for use.

    Environment variables:
        OTEL_SERVICE_NAME: Override service_name parameter
        OTEL_EXPORTER_OTLP_ENDPOINT: Default OTLP endpoint
        JAEGER_ENDPOINT: Default Jaeger endpoint
        GENAI_MEMORY_CAPTURE_CONTENT: Enable content capture ('true'/'false')
        GENAI_MEMORY_EXPORTERS: Comma-separated exporters (overrides use_* flags)

    Args:
        service_name: Name of the service for traces (default: 'genai-memory-prototype')
        service_version: Version of the service (default: '0.1.0')
        use_console: Enable console exporter (default: True)
        use_otlp: Enable OTLP exporter (default: False)
        otlp_endpoint: OTLP collector endpoint (default: from env or localhost:4317)
        use_jaeger: Enable Jaeger exporter (default: False)
        jaeger_endpoint: Jaeger endpoint (default: from env or localhost:14268)
        capture_content: Enable sensitive content capture (default: False)
        exporters: Optional exporter list (overrides use_* flags). Supported:
                   console, otlp, jaeger, appinsights, laminar, langfuse, traceloop
        use_simple_processor: Use SimpleSpanProcessor instead of batch (for testing)

    Returns:
        trace.Tracer: Configured tracer instance

    Example:
        # Development setup with console output
        tracer = setup_tracing(service_name="my-agent")

        # Production setup with OTLP
        tracer = setup_tracing(
            service_name="my-agent",
            use_console=False,
            use_otlp=True,
        )

        # Testing setup with immediate export
        tracer = setup_tracing(
            service_name="test-agent",
            use_simple_processor=True,
        )
    """
    # Allow env override for demo runs (immediate export).
    if os.getenv("GENAI_MEMORY_USE_SIMPLE_PROCESSOR", "false").lower() == "true":
        use_simple_processor = True

    # Resolve service name from environment
    resolved_service_name = os.getenv("OTEL_SERVICE_NAME", service_name)

    exporters_env = os.getenv("GENAI_MEMORY_EXPORTERS")
    requested_exporters = exporters if exporters is not None else (
        _parse_exporters(exporters_env) if exporters_env else None
    )

    if requested_exporters:
        print("=" * 70)
        print("  OpenTelemetry Tracing Bootstrap (GenAI Memory)")
        print("=" * 70)

        if "traceloop" in requested_exporters:
            unsupported = [e for e in requested_exporters if e not in {"traceloop", "console"}]
            if unsupported:
                print(
                    "[WARN] Traceloop selected; skipping other exporters in this run: "
                    + ", ".join(unsupported)
                )

            provider = _configure_traceloop(
                service_name=resolved_service_name,
                service_version=service_version,
                capture_content=capture_content,
                disable_batch=use_simple_processor,
            )
            if provider is not None:
                if "console" in requested_exporters:
                    try:
                        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
                        print("[OK] Console: enabled")
                    except Exception as e:
                        print(f"[WARN] Console: failed to attach - {e}")

                atexit.register(shutdown_tracing)
                return trace.get_tracer(
                    instrumenting_module_name="genai_memory_otel",
                    instrumenting_library_version=service_version,
                )

            print("[WARN] Traceloop requested but not configured; continuing without Traceloop")
            requested_exporters = [e for e in requested_exporters if e != "traceloop"]

    # Create resource with service information
    resource = Resource.create({
        SERVICE_NAME: resolved_service_name,
        SERVICE_VERSION: service_version,
        "genai.memory.capture_content": str(capture_content).lower(),
    })

    # Create and configure tracer provider
    provider = TracerProvider(resource=resource)

    # Ensure spans are flushed on process exit
    atexit.register(provider.shutdown)

    processor_class = SimpleSpanProcessor if use_simple_processor else BatchSpanProcessor
    configured_exporters: List[str] = []

    # Multi-backend mode: GENAI_MEMORY_EXPORTERS / exporters param
    if requested_exporters:
        for exporter_name in requested_exporters:
            if exporter_name == "console":
                provider.add_span_processor(processor_class(ConsoleSpanExporter()))
                configured_exporters.append("Console")
                print("[OK] Console: enabled")

            elif exporter_name == "appinsights":
                exporter = _get_azure_exporter()
                if exporter:
                    provider.add_span_processor(processor_class(exporter))
                    configured_exporters.append("App Insights")

            elif exporter_name == "laminar":
                exporter = _get_laminar_exporter()
                if exporter:
                    provider.add_span_processor(processor_class(exporter))
                    configured_exporters.append("Laminar")

            elif exporter_name == "langfuse":
                exporter = _get_langfuse_exporter()
                if exporter:
                    provider.add_span_processor(processor_class(exporter))
                    configured_exporters.append("Langfuse")

            elif exporter_name == "otlp":
                use_otlp = True

            elif exporter_name == "jaeger":
                use_jaeger = True

            else:
                print(f"[WARN] Unknown exporter in GENAI_MEMORY_EXPORTERS: {exporter_name}")

    # Add console exporter (legacy mode)
    if not requested_exporters and use_console:
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(processor_class(console_exporter))
        configured_exporters.append("Console")

    # Add OTLP exporter
    if use_otlp:
        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

            endpoint = otlp_endpoint or os.getenv(
                "OTEL_EXPORTER_OTLP_ENDPOINT",
                "http://localhost:4317"
            )
            otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
            provider.add_span_processor(processor_class(otlp_exporter))
            configured_exporters.append("OTLP")
        except ImportError:
            raise ImportError(
                "OTLP exporter requires opentelemetry-exporter-otlp-proto-grpc. "
                "Install with: pip install opentelemetry-exporter-otlp-proto-grpc"
            )

    # Add Jaeger exporter (legacy)
    if use_jaeger:
        try:
            from opentelemetry.exporter.jaeger.thrift import JaegerExporter

            endpoint = jaeger_endpoint or os.getenv(
                "JAEGER_ENDPOINT",
                "http://localhost:14268/api/traces"
            )
            jaeger_exporter = JaegerExporter(
                collector_endpoint=endpoint,
            )
            provider.add_span_processor(processor_class(jaeger_exporter))
            configured_exporters.append("Jaeger")
        except ImportError:
            raise ImportError(
                "Jaeger exporter requires opentelemetry-exporter-jaeger. "
                "Install with: pip install opentelemetry-exporter-jaeger"
            )

    # Set the global tracer provider
    trace.set_tracer_provider(provider)

    if requested_exporters:
        print("-" * 70)
        if configured_exporters:
            print(f"[OK] Active exporters: {', '.join(configured_exporters)}")
        else:
            print("[WARN] No exporters configured! Check GENAI_MEMORY_EXPORTERS and credentials.")
        print("=" * 70 + "\n")

    # Return a tracer from this provider
    return trace.get_tracer(
        instrumenting_module_name="genai_memory_otel",
        instrumenting_library_version=service_version,
    )


def should_capture_content() -> bool:
    """
    Check if sensitive content capture is enabled via environment.

    Content capture is opt-in due to privacy concerns. This function
    checks the GENAI_MEMORY_CAPTURE_CONTENT environment variable.

    Returns:
        bool: True if content capture is enabled

    Example:
        if should_capture_content():
            span.set_attribute(MemoryAttributes.MEMORY_CONTENT, content)
    """
    return os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true"


def get_tracer(name: str = __name__) -> trace.Tracer:
    """
    Get a tracer from the configured provider.

    This is a convenience function for getting additional tracers
    after setup_tracing has been called.

    Args:
        name: Tracer name (default: calling module name)

    Returns:
        trace.Tracer: Tracer instance

    Example:
        tracer = get_tracer("my_module")
    """
    return trace.get_tracer(name)


def shutdown_tracing() -> None:
    """
    Shutdown the tracer provider and flush pending spans.

    Call this at application shutdown to ensure all spans are exported.

    Example:
        import atexit
        atexit.register(shutdown_tracing)
    """
    provider = trace.get_tracer_provider()
    if hasattr(provider, 'shutdown'):
        provider.shutdown()


class TracingConfig:
    """
    Configuration class for tracing setup.

    This class provides a structured way to configure tracing options
    and can be used with dependency injection frameworks.

    Attributes:
        service_name: Name of the service
        service_version: Version of the service
        use_console: Enable console exporter
        use_otlp: Enable OTLP exporter
        otlp_endpoint: OTLP collector endpoint
        use_jaeger: Enable Jaeger exporter
        jaeger_endpoint: Jaeger endpoint
        capture_content: Enable content capture
    """

    def __init__(
        self,
        service_name: str = "genai-memory-prototype",
        service_version: str = "0.1.0",
        use_console: bool = True,
        use_otlp: bool = False,
        otlp_endpoint: Optional[str] = None,
        use_jaeger: bool = False,
        jaeger_endpoint: Optional[str] = None,
        capture_content: bool = False,
        exporters: Optional[List[str]] = None,
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.use_console = use_console
        self.use_otlp = use_otlp
        self.otlp_endpoint = otlp_endpoint
        self.use_jaeger = use_jaeger
        self.jaeger_endpoint = jaeger_endpoint
        self.capture_content = capture_content
        self.exporters = exporters

    @classmethod
    def from_env(cls) -> "TracingConfig":
        """
        Create configuration from environment variables.

        Environment variables:
            OTEL_SERVICE_NAME: Service name
            OTEL_SERVICE_VERSION: Service version
            GENAI_MEMORY_USE_CONSOLE: Use console exporter ('true'/'false')
            GENAI_MEMORY_USE_OTLP: Use OTLP exporter ('true'/'false')
            OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint
            GENAI_MEMORY_USE_JAEGER: Use Jaeger exporter ('true'/'false')
            JAEGER_ENDPOINT: Jaeger endpoint
            GENAI_MEMORY_CAPTURE_CONTENT: Capture content ('true'/'false')

        Returns:
            TracingConfig: Configuration from environment
        """
        exporters_env = os.getenv("GENAI_MEMORY_EXPORTERS")
        return cls(
            service_name=os.getenv("OTEL_SERVICE_NAME", "genai-memory-prototype"),
            service_version=os.getenv("OTEL_SERVICE_VERSION", "0.1.0"),
            use_console=os.getenv("GENAI_MEMORY_USE_CONSOLE", "true").lower() == "true",
            use_otlp=os.getenv("GENAI_MEMORY_USE_OTLP", "false").lower() == "true",
            otlp_endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
            use_jaeger=os.getenv("GENAI_MEMORY_USE_JAEGER", "false").lower() == "true",
            jaeger_endpoint=os.getenv("JAEGER_ENDPOINT"),
            capture_content=os.getenv("GENAI_MEMORY_CAPTURE_CONTENT", "false").lower() == "true",
            exporters=_parse_exporters(exporters_env) if exporters_env else None,
        )

    def setup(self) -> trace.Tracer:
        """
        Set up tracing with this configuration.

        Returns:
            trace.Tracer: Configured tracer instance
        """
        return setup_tracing(
            service_name=self.service_name,
            service_version=self.service_version,
            use_console=self.use_console,
            use_otlp=self.use_otlp,
            otlp_endpoint=self.otlp_endpoint,
            use_jaeger=self.use_jaeger,
            jaeger_endpoint=self.jaeger_endpoint,
            capture_content=self.capture_content,
            exporters=self.exporters,
        )
