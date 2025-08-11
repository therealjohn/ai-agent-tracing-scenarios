import os, time, json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "_shared"))
from tracing import init_tracing, get_tracer

ENDPOINT = os.environ["AZURE_AI_CHAT_ENDPOINT"]
KEY = os.environ["AZURE_AI_CHAT_KEY"]
MODEL = os.getenv("MODEL_NAME")

init_tracing("scenario06")
tracer = get_tracer("scenario06")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def parse_doc(doc: str, timeout_s=0.5) -> dict:
    start = time.time()
    with tracer.start_span("tool.doc_parser", attributes={"timeout_s": timeout_s}):
        time.sleep(0.8)  # simulate a slow external call
        if time.time() - start > timeout_s:
            raise TimeoutError("parser timeout")
        return {"sections": ["A", "B", "C"]}

def analyze(doc: str):
    try:
        parsed = parse_doc(doc)
    except Exception as e:
        with tracer.start_span("tool.doc_parser.error", attributes={"error": str(e)}):
            parsed = {"sections": ["A"]}  # BUG: swallow error and degrade silently
    msg = client.complete(
        model=MODEL,
        messages=[
            SystemMessage("Summarize each section found."),
            UserMessage(json.dumps(parsed))
        ],
    )
    return msg.choices[0].message.content[0].text

if __name__ == "__main__":
    print(analyze("dummy"))
