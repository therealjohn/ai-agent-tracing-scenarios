import os
import json
import random
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

# Initialize tracing and client
init_tracing("scenario_02")
tracer = get_tracer("scenario_02")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

# Knowledge base
KB = {
    "pto_policy": "Employees accrue 1.5 days PTO per month. Carryover up to 5 days.",
    "expense_policy": "Travel meals capped at $60/day. Receipts required."
}

def llm(messages):
    return client.complete(model=MODEL, messages=messages)

@tracer.start_as_current_span("retrieval")
def retrieval(query: str) -> str:
    current_span = trace.get_current_span()
    current_span.set_attribute("query", query)
    
    with tracer.start_span("knowledge_base_lookup") as kb_span:
        result = KB.get(query, "")
        kb_span.set_attribute("found", bool(result))
        kb_span.set_attribute("result_length", len(result))
        
    current_span.set_attribute("result_found", bool(result))
    return result

@tracer.start_as_current_span("scenario_02")
def answer_question(topic: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("question.topic", topic)
    current_span.set_attribute("scenario.name", "hallucination_skips_retrieval")
    
    question = f"What's our {topic.replace('_', ' ')}?"
    use_kb = random.choice([True, False])
    current_span.set_attribute("retrieval.used", use_kb)

    # Construct system prompt based on retrieval usage
    with tracer.start_span("construct_prompt") as prompt_span:
        if use_kb:
            sys_prompt = "You are an internal policy assistant. Cite retrieved snippets verbatim.\nDO NOT use external knowledge.\n"
            prompt_variation = "strict"
        else:
            sys_prompt = "You are an internal policy assistant. Cite retrieved snippets verbatim.\nBe brief and helpful.\n"
            prompt_variation = "flexible"
        prompt_span.set_attribute("system_prompt_variation", prompt_variation)

    # Perform retrieval if needed
    kb_snippet = retrieval(topic) if use_kb else ""
    current_span.set_attribute("retrieval.found_content", bool(kb_snippet))
    if kb_snippet:
        current_span.set_attribute("retrieval.content_length", len(kb_snippet))

    # Build messages
    messages = [SystemMessage(sys_prompt), UserMessage(question)]
    if kb_snippet:
        messages.append(AssistantMessage(f"[retrieved]\n{kb_snippet}"))

    # Add user message event
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", question)

    # Get LLM response
    resp = llm(messages)
    content = resp.choices[0].message.content
    
    # Add choice event
    add_choice_event(current_span, content)
    current_span.set_attribute("gen_ai.usage.total_tokens", resp.usage.total_tokens)
    
    return content

if __name__ == "__main__":
    out = answer_question("pto_policy")
    print(out)
