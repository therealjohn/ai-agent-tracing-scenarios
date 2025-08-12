import os
import time
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
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
init_tracing("scenario03")
tracer = get_tracer("scenario03")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def llm(messages):
    response = client.complete(model=MODEL, messages=messages)
    content = response.choices[0].message.content
    
    # Handle both string and list content formats
    return content if isinstance(content, str) else (
        content[0].text if hasattr(content[0], 'text') else str(content[0])
    )

@tracer.start_as_current_span("agent.planner")
def planner(task: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("task", task)
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", task)
    
    result = llm([SystemMessage("Planner. Output bullet plan only."), UserMessage(task)])
    add_choice_event(current_span, result)
    return result

@tracer.start_as_current_span("agent.researcher")
def researcher(plan: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("plan", plan)
    current_span.set_attribute("bug.double_pass", True)
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", plan)
    
    # BUG: needless double-pass loop adds latency
    result = ""
    for i in range(2):  # should be 1
        with tracer.start_span(f"research_pass_{i+1}") as pass_span:
            pass_span.set_attribute("pass_number", i+1)
            time.sleep(0.8)  # simulate IO
            result = llm([SystemMessage("Researcher. Extract key facts only."), UserMessage(plan)])
    
    add_choice_event(current_span, result)
    return result

@tracer.start_as_current_span("agent.summarizer")
def summarizer(facts: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("facts", facts)
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", facts)
    
    result = llm([SystemMessage("Summarizer. 5 concise bullets."), UserMessage(facts)])
    add_choice_event(current_span, result)
    return result

@tracer.start_as_current_span("scenario_03")
def main():
    current_span = trace.get_current_span()
    current_span.set_attribute("scenario.name", "slow_multi_step_reasoning")
    
    task = "Compare two approaches to caching API responses."
    p = planner(task)
    r = researcher(p)
    s = summarizer(r)
    return s

if __name__ == "__main__":
    result = main()
    print(result)
