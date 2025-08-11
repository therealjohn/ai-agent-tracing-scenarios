# main.py
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv; load_dotenv()

### Set up for OpenTelemetry tracing ###
# Enable content recording for prompts and completions
os.environ["AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED"] = "true"
os.environ["AZURE_SDK_TRACING_IMPLEMENTATION"] = "opentelemetry"

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Set up the tracer provider with OTLP exporter for AI Toolkit
resource = Resource(attributes={
    "service.name": "ai-agent-tracing-scenarios"
})
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4321/v1/traces",
)
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Instrument Azure AI Inference client
from azure.ai.inference.tracing import AIInferenceInstrumentor
AIInferenceInstrumentor().instrument()
### Set up for OpenTelemetry tracing ###

def main():
    endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_AI_CHAT_KEY"]
    model = os.getenv("MODEL_NAME")  # optional in some setups

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("Explain the benefits of continuous integration in 3 bullet points.")
    ]

    response = client.complete(model=model, messages=messages)
    text = response.choices[0].message.content[0].text
    print(json.dumps({"summary": text.strip()}, indent=2))

if __name__ == "__main__":
    main()
