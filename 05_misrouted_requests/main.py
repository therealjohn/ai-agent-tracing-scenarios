import os
import re
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
init_tracing("scenario05")
tracer = get_tracer("scenario05")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

@tracer.start_as_current_span("router.classify")
def route(question: str) -> str:
    current_span = trace.get_current_span()
    current_span.set_attribute("question", question)
    
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", question)
    
    resp = client.complete(
        model=MODEL,
        messages=[
            SystemMessage("Return ONLY one token: FINANCE or TECH."),
            UserMessage(question)
        ],
    )
    
    content = resp.choices[0].message.content
    # Handle both string and list content formats
    msg = content.strip() if isinstance(content, str) else (
        content[0].text.strip() if hasattr(content[0], 'text') else str(content[0]).strip()
    )
    
    add_choice_event(current_span, content)
    current_span.set_attribute("classification", msg)
    return msg

@tracer.start_as_current_span("scenario_05")
def handle(question: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("scenario.name", "misrouted_requests")
    current_span.set_attribute("question", question)
    
    label = route(question)
    
    with tracer.start_span("router.dispatch") as dispatch_span:
        dispatch_span.set_attribute("original_label", label)
        
        # BUG: sloppy parsing flips labels if text contains both words
        original_label = label
        if re.search(r"TECH.*FINANCE|FINANCE.*TECH", label):
            label = "TECH" if "FINANCE" in label else "FINANCE"  # nonsense flip
            dispatch_span.set_attribute("bug_triggered", True)
            dispatch_span.set_attribute("flipped_to", label)
        
        target = "FinanceBot" if label.startswith("FIN") else "TechBot"
        dispatch_span.set_attribute("routed_to", target)
        
        result = f"[{target}] Answer to: {question}"
        current_span.set_attribute("response", result)
        return result

if __name__ == "__main__":
    result = handle("Is our TECH budget approved for Q4?")
    print(result)
