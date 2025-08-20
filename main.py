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

total_tokens = 0

# Initialize tracing
init_tracing("scenario_04")
tracer = get_tracer("scenario_04")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def llm(messages):
    response = client.complete(model=MODEL, messages=messages)
    content = response.choices[0].message.content
    global total_tokens 
    total_tokens += response.usage.total_tokens

    return str(content)

@tracer.start_as_current_span("agent.planner")
def planner(task: str):
    result = llm([SystemMessage("Planner. Output bullet plan only."), UserMessage(task)])

    return result

@tracer.start_as_current_span("agent.researcher")
def researcher(plan: str):
    # BUG: needless double-pass loop adds latency
    result = ""
    for i in range(2):  # should be 1
        time.sleep(1.5)  # simulate IO
        result = llm([SystemMessage("Researcher. Extract key facts only."), UserMessage(plan)])
    
    return result

@tracer.start_as_current_span("agent.summarizer")
def summarizer(facts: str):
    result = llm([SystemMessage("Summarizer. 5 concise bullets."), UserMessage(facts)])

    return result

@tracer.start_as_current_span("scenario_04")
def main():
    global total_tokens
    total_tokens = 0
    task = "Compare two approaches to caching API responses."

    current_span = trace.get_current_span()
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", task)

    p = planner(task)
    r = researcher(p)
    s = summarizer(r)

    add_choice_event(current_span, s)
    current_span.set_attribute("gen_ai.usage.total_tokens", total_tokens)
    return s

if __name__ == "__main__":
    result = main()
    print(result)
