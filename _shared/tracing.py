# _shared/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from azure.ai.inference.tracing import AIInferenceInstrumentor

_IS_INIT = False

def init_tracing(service_name: str = "ai-agent-scenarios"):
    global _IS_INIT
    if _IS_INIT:
        return
    provider = TracerProvider()
    trace.set_tracer_provider(provider)
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    # Instrument Azure AI Inference client spans
    AIInferenceInstrumentor().instrument()
    _IS_INIT = True

def get_tracer(name: str):
    return trace.get_tracer(name)
