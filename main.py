import os
import time
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
init_tracing("scenario_06")
tracer = get_tracer("scenario_06")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def parse_doc(doc: str, timeout_s=0.5) -> dict:
    start = time.time()
    with tracer.start_span("tool.doc_parser") as span:
        span.set_attribute("timeout_s", timeout_s)
        span.set_attribute("doc", doc)
        
        time.sleep(0.8)  # simulate a slow external call
        elapsed = time.time() - start
        span.set_attribute("elapsed_time", elapsed)
        
        if elapsed > timeout_s:
            span.set_attribute("timed_out", True)
            raise TimeoutError("parser timeout")
        
        result = {"sections": ["A", "B", "C"]}
        span.set_attribute("sections_found", len(result["sections"]))
        return result

@tracer.start_as_current_span("scenario_05")
def analyze(doc: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("scenario.name", "tool_timeout_swallowed")
    current_span.set_attribute("document", doc)
    
    try:
        parsed = parse_doc(doc)
        current_span.set_attribute("parsing_successful", True)
    except Exception as e:
        with tracer.start_span("tool.doc_parser.error") as error_span:
            error_span.set_attribute("error_type", type(e).__name__)
            error_span.set_attribute("error_message", str(e))
            error_span.set_attribute("swallowed_error", True)
            
            parsed = {"sections": ["A"]}  # BUG: swallow error and degrade silently
            current_span.set_attribute("parsing_successful", False)
            current_span.set_attribute("fallback_used", True)
    
    user_input = json.dumps(parsed)
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", user_input)
    
    msg = client.complete(
        model=MODEL,
        messages=[
            SystemMessage("Summarize each section found."),
            UserMessage(user_input)
        ],
    )
    
    content = msg.choices[0].message.content
    
    add_choice_event(current_span, content)
    current_span.set_attribute("gen_ai.usage.total_tokens", msg.usage.total_tokens)
    
    return content

if __name__ == "__main__":
    result = analyze("dummy")
    print(result)
