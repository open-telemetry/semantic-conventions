#!/usr/bin/env python3
"""
OpenTelemetry Bootstrap Module for Multi-Backend Trace Export

Configures a single global TracerProvider with exporters for:
- Azure Application Insights (connection string)
- Laminar (LMNR OTLP ingest)
- Langfuse (OTLP HTTP with Basic Auth)
- Traceloop (OpenLLMetry SDK)
- Console (for local debugging)

Usage:
    from otel_bootstrap import configure_tracing, ExporterConfig

    configure_tracing(
        service_name="my-service",
        exporters=[ExporterConfig.APP_INSIGHTS, ExporterConfig.LAMINAR],
        enable_console=True
    )
"""

import os
import base64
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
    BatchSpanProcessor,
)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION


class ExporterType(Enum):
    """Available trace exporters."""
    CONSOLE = "console"
    APP_INSIGHTS = "appinsights"
    LAMINAR = "laminar"
    LANGFUSE = "langfuse"
    TRACELOOP = "traceloop"


@dataclass
class TracingConfig:
    """Configuration for tracing bootstrap."""
    service_name: str = "genai-security-guardian-demos"
    service_version: str = "0.1.0"
    environment: str = "prototype"
    disable_batch: bool = True  # Use SimpleSpanProcessor for immediate export


# Global state
_configured = False
_provider: Optional[TracerProvider] = None


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
        print(f"[SKIP] App Insights: azure-monitor-opentelemetry-exporter not installed or incompatible")
        print(f"       Error: {e}")
        print("       Note: Traceloop SDK may have installed incompatible OTel versions")
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

        # Laminar uses gRPC on port 8443
        exporter = OTLPSpanExporter(
            endpoint="https://api.lmnr.ai:8443",
            headers={"authorization": f"Bearer {api_key}"},
        )
        print("[OK] Laminar: configured (api.lmnr.ai:8443)")
        return exporter
    except ImportError:
        print("[SKIP] Laminar: opentelemetry-exporter-otlp-proto-grpc not installed")
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

        # Langfuse requires Basic Auth: base64(public_key:secret_key)
        auth_string = f"{public_key}:{secret_key}"
        auth_bytes = auth_string.encode('utf-8')
        auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')

        endpoint = f"{base_url}/api/public/otel/v1/traces"

        exporter = OTLPSpanExporter(
            endpoint=endpoint,
            headers={"Authorization": f"Basic {auth_b64}"},
        )
        print(f"[OK] Langfuse: configured ({base_url})")
        return exporter
    except ImportError:
        print("[SKIP] Langfuse: opentelemetry-exporter-otlp-proto-http not installed")
        return None
    except Exception as e:
        print(f"[SKIP] Langfuse: failed to configure - {e}")
        return None


def _configure_traceloop(service_name: str, service_version: str, environment: str, disable_batch: bool):
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
                "deployment.environment": environment,
            },
        )
        print("[OK] Traceloop: SDK initialized")
        return trace.get_tracer_provider()
    except ImportError:
        print("[SKIP] Traceloop: traceloop-sdk not installed")
        return None
    except Exception as e:
        print(f"[SKIP] Traceloop: failed to configure - {e}")
        return None


def configure_tracing(
    service_name: str = "genai-security-guardian-demos",
    service_version: str = "0.1.0",
    environment: str = "prototype",
    exporters: Optional[List[ExporterType]] = None,
    enable_console: bool = False,
    disable_batch: bool = True,
) -> TracerProvider:
    """
    Configure OpenTelemetry tracing with specified exporters.

    Args:
        service_name: Name of the service for resource attributes
        service_version: Version of the service
        environment: Deployment environment (e.g., "prototype", "production")
        exporters: List of exporters to configure. If None, configures all available.
        enable_console: Also enable console output for local debugging
        disable_batch: Use SimpleSpanProcessor for immediate export (recommended for demos)

    Returns:
        The configured TracerProvider
    """
    global _configured, _provider

    if _configured and _provider:
        print("[INFO] Tracing already configured, returning existing provider")
        return _provider

    print("=" * 70)
    print("  OpenTelemetry Tracing Bootstrap")
    print("=" * 70)

    if exporters and ExporterType.TRACELOOP in exporters:
        unsupported = [e for e in exporters if e not in {ExporterType.TRACELOOP, ExporterType.CONSOLE}]
        if unsupported:
            print(
                "[WARN] Traceloop selected; skipping other exporters in this run: "
                + ", ".join(e.value for e in unsupported)
            )

        tl_provider = _configure_traceloop(service_name, service_version, environment, disable_batch)
        if tl_provider:
            if enable_console or ExporterType.CONSOLE in exporters:
                try:
                    tl_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
                    print("[OK] Console: enabled")
                    active = ["Console", "Traceloop"]
                except Exception as e:
                    print(f"[WARN] Console: failed to attach - {e}")
                    active = ["Traceloop"]
            else:
                active = ["Traceloop"]

            _provider = tl_provider
            _configured = True

            print("-" * 70)
            print(f"[OK] Active exporters: {', '.join(active)}")
            print("=" * 70 + "\n")
            return tl_provider

        print("[WARN] Traceloop requested but not configured; continuing without Traceloop")
        exporters = [e for e in exporters if e != ExporterType.TRACELOOP]

    # Create resource
    resource = Resource.create({
        SERVICE_NAME: service_name,
        SERVICE_VERSION: service_version,
        "deployment.environment": environment,
    })

    # Create provider
    provider = TracerProvider(resource=resource)

    # Determine which exporters to configure
    if exporters is None:
        # Auto-detect: configure all backends that have credentials set
        exporters = [
            ExporterType.APP_INSIGHTS,
            ExporterType.LAMINAR,
            ExporterType.LANGFUSE,
        ]
        if os.environ.get("TRACELOOP_API_KEY"):
            print("[INFO] Traceloop detected; run separately with --exporters traceloop")

    configured_exporters = []

    # Add console exporter if requested
    if enable_console:
        processor = SimpleSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        configured_exporters.append("Console")
        print("[OK] Console: enabled")

    # Configure each exporter
    for exp_type in exporters:
        if exp_type == ExporterType.CONSOLE:
            if not enable_console:
                processor = SimpleSpanProcessor(ConsoleSpanExporter())
                provider.add_span_processor(processor)
                configured_exporters.append("Console")
                print("[OK] Console: enabled")

        elif exp_type == ExporterType.APP_INSIGHTS:
            exporter = _get_azure_exporter()
            if exporter:
                processor = SimpleSpanProcessor(exporter) if disable_batch else BatchSpanProcessor(exporter)
                provider.add_span_processor(processor)
                configured_exporters.append("App Insights")

        elif exp_type == ExporterType.LAMINAR:
            exporter = _get_laminar_exporter()
            if exporter:
                processor = SimpleSpanProcessor(exporter) if disable_batch else BatchSpanProcessor(exporter)
                provider.add_span_processor(processor)
                configured_exporters.append("Laminar")

        elif exp_type == ExporterType.LANGFUSE:
            exporter = _get_langfuse_exporter()
            if exporter:
                processor = SimpleSpanProcessor(exporter) if disable_batch else BatchSpanProcessor(exporter)
                provider.add_span_processor(processor)
                configured_exporters.append("Langfuse")

        elif exp_type == ExporterType.TRACELOOP:
            print("[INFO] Traceloop detected; run separately with --exporters traceloop")

    # Set global provider
    trace.set_tracer_provider(provider)
    _provider = provider
    _configured = True

    print("-" * 70)
    if configured_exporters:
        print(f"[OK] Active exporters: {', '.join(configured_exporters)}")
    else:
        print("[WARN] No exporters configured! Set environment variables for backends.")
    print("=" * 70 + "\n")

    return provider


def get_provider() -> Optional[TracerProvider]:
    """Get the configured TracerProvider."""
    global _provider
    return _provider


def reset_tracing():
    """Reset tracing state (useful for testing)."""
    global _configured, _provider
    _configured = False
    _provider = None


# Environment variable names for reference
ENV_VARS = {
    "App Insights": "APPLICATIONINSIGHTS_CONNECTION_STRING",
    "Laminar": "LMNR_PROJECT_API_KEY",
    "Langfuse": ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_BASE_URL"],
    "Traceloop": "TRACELOOP_API_KEY",
}


if __name__ == "__main__":
    print("OpenTelemetry Bootstrap Module")
    print("\nRequired environment variables by backend:")
    for backend, vars in ENV_VARS.items():
        if isinstance(vars, list):
            print(f"  {backend}: {', '.join(vars)}")
        else:
            print(f"  {backend}: {vars}")

    print("\nUsage:")
    print("  from otel_bootstrap import configure_tracing")
    print("  configure_tracing(service_name='my-service')")
