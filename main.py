import os
import json
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from opentelemetry import trace

# Load environment and setup path
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _shared.tracing import add_choice_event, add_gen_ai_event, init_tracing, get_tracer

# Configuration
ENDPOINT = os.environ["MODEL_ENDPOINT"]
KEY = os.environ["API_CREDENTIAL_TOKEN"]
MODEL = os.getenv("MODEL_NAME")

# Initialize tracing
init_tracing("scenario_04")
tracer = get_tracer("scenario_04")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

@tracer.start_as_current_span("scenario_04")
def main():
    current_span = trace.get_current_span()
    
    query = "Summarize the benefits of CI/CD and trunk-based development."
    messages = [
        SystemMessage("You write detailed summaries of 400-600 words."),
        UserMessage(query)
    ]
    
    # Add user message event
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", query)
    
    # Intentionally low output tokens to trigger length truncation
    resp = client.complete(model=MODEL, messages=messages, max_tokens=50)
    choice = resp.choices[0]
    
    content = choice.message.content
    
    # Add choice event
    add_choice_event(current_span, content)
    current_span.set_attribute("gen_ai.usage.total_tokens", resp.usage.total_tokens)

    # Log truncation information
    finish_reason = getattr(choice, "finish_reason", "unknown")
    
    return content

if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
