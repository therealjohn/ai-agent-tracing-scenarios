import os, json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
import random

from dotenv import load_dotenv; load_dotenv()

import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "_shared"))
from tracing import init_tracing, get_tracer

ENDPOINT = os.environ["AZURE_AI_CHAT_ENDPOINT"]
KEY = os.environ["AZURE_AI_CHAT_KEY"]
MODEL = os.getenv("MODEL_NAME")  # optional for some endpoints

init_tracing("scenario01")
tracer = get_tracer("scenario01")

client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def llm(messages):
    return client.complete(model=MODEL, messages=messages)

def retrieval(query: str) -> str:
    # Fake "KB retrieval": pretend to fetch policy text (another LLM call in a real app)
    # We trace this explicitly as a step developers should notice.
    with tracer.start_span("retrieval.lookup"):
        kb = {
            "pto_policy": "Employees accrue 1.5 days PTO per month. Carryover up to 5 days.",
            "expense_policy": "Travel meals capped at $60/day. Receipts required."
        }
        return kb.get(query, "")

def answer_question(topic: str):
    # Randomly "skip" retrieval path to simulate flaky behavior
    use_kb = random.choice([True, False])

    sys_prompt = (
        "You are an internal policy assistant. Cite retrieved snippets verbatim.\n"
        + ("DO NOT use external knowledge.\n" if use_kb else "Be brief and helpful.\n")  # bug-inducing variance
    )

    kb_snippet = retrieval(topic) if use_kb else ""

    messages = [
        SystemMessage(sys_prompt),
        UserMessage(f"What's our {topic.replace('_',' ')}?")
    ]
    if kb_snippet:
        messages.append(AssistantMessage(f"[retrieved]\n{kb_snippet}"))

    resp = llm(messages)
    content = resp.choices[0].message.content
    
    # Handle both string and list content formats
    if isinstance(content, str):
        text = content
    else:
        # If content is a list, get the text from the first item
        text = content[0].text if hasattr(content[0], 'text') else str(content[0])
    return {"use_kb": use_kb, "kb_snippet": kb_snippet, "answer": content}

if __name__ == "__main__":
    out = answer_question("pto_policy")
    print(json.dumps(out, indent=2))
