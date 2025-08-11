import os, time
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "_shared"))
from tracing import init_tracing, get_tracer

ENDPOINT = os.environ["AZURE_AI_CHAT_ENDPOINT"]
KEY = os.environ["AZURE_AI_CHAT_KEY"]
MODEL = os.getenv("MODEL_NAME")

init_tracing("scenario03")
tracer = get_tracer("scenario03")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def llm(messages):
    return client.complete(model=MODEL, messages=messages).choices[0].message.content[0].text

def planner(task: str):
    with tracer.start_span("agent.planner"):
        return llm([SystemMessage("Planner. Output bullet plan only."), UserMessage(task)])

def researcher(plan: str):
    with tracer.start_span("agent.researcher"):
        # BUG: needless double-pass loop adds latency
        result = ""
        for i in range(2):  # should be 1
            time.sleep(0.8)  # simulate IO
            result = llm([SystemMessage("Researcher. Extract key facts only."), UserMessage(plan)])
        return result

def summarizer(facts: str):
    with tracer.start_span("agent.summarizer"):
        return llm([SystemMessage("Summarizer. 5 concise bullets."), UserMessage(facts)])

if __name__ == "__main__":
    p = planner("Compare two approaches to caching API responses.")
    r = researcher(p)
    s = summarizer(r)
    print(s)
