# _shared/tracing.py
import json
import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from azure.ai.inference.tracing import AIInferenceInstrumentor

_IS_INIT = False

def init_tracing(service_name: str = "ai-agent-scenarios"):
    """
    Initialize OpenTelemetry tracing with Azure AI Inference instrumentation.
    
    This sets up:
    - Automatic instrumentation for Azure AI Inference SDK calls
    - OTLP exporter pointing to AI Toolkit (localhost:4321)
    - Content recording for prompts and completions
    """
    global _IS_INIT
    if _IS_INIT:
        return
    
    # Set up environment variables for Azure AI Inference tracing
    # This enables capturing prompt and completion content in traces
    os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"
    os.environ["AZURE_SDK_TRACING_IMPLEMENTATION"] = "opentelemetry"
    os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"
    
    # Configure resource with service name and version info
    resource = Resource(attributes={
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": "development"
    })
    
    # Set up tracer provider with resource
    provider = TracerProvider(resource=resource)
    
    # Configure OTLP exporter to send traces to AI Toolkit
    # AI Toolkit expects traces on http://localhost:4321/v1/traces
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4321/v1/traces",
        timeout=30  # Add timeout for better reliability
    )
    
    # Use BatchSpanProcessor for better performance in production
    processor = BatchSpanProcessor(
        otlp_exporter,
        max_queue_size=2048,
        max_export_batch_size=512,
        export_timeout_millis=30000
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    
    # Instrument Azure AI Inference client - this automatically creates spans for API calls
    # No need to manually trace LLM calls when this is enabled
    AIInferenceInstrumentor().instrument()
    
    _IS_INIT = True
    print(f"[OK] Tracing initialized for service: {service_name}")
    print("[OK] AI Toolkit tracing viewer should be open to collect traces")

def get_tracer(name: str):
    """Get a tracer instance for creating custom spans for business logic."""
    return trace.get_tracer(name)

def add_gen_ai_event(span, event_name, role, content):
    """Helper function to add standardized gen_ai events"""
    span.add_event(
        event_name,
        {
            "gen_ai.system": "az.ai.inference",
            "gen_ai.event.content": json.dumps({"role": role, "content": content})
        }
    )

def add_choice_event(span, content):
    """Helper function to add gen_ai.choice event"""
    span.add_event(
        "gen_ai.choice",
        {
            "gen_ai.system": "az.ai.inference",
            "gen_ai.event.content": json.dumps({
                "message": {"content": str(content)},
                "finish_reason": "stop",
                "index": 0
            })
        }
    )