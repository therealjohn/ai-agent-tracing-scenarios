import os, re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
import sys
from dotenv import load_dotenv; load_dotenv()

sys.path.append(str(Path(__file__).resolve().parents[1] / "_shared"))
from tracing import init_tracing, get_tracer

ENDPOINT = os.environ["AZURE_AI_CHAT_ENDPOINT"]
KEY = os.environ["AZURE_AI_CHAT_KEY"]
MODEL = os.getenv("MODEL_NAME")

init_tracing("scenario05")
tracer = get_tracer("scenario05")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def route(question: str) -> str:
    with tracer.start_span("router.classify"):
        msg = client.complete(
            model=MODEL,
            messages=[
                SystemMessage("Return ONLY one token: FINANCE or TECH."),
                UserMessage(question)
            ],
        ).choices[0].message.content[0].text.strip()
        return msg

def handle(question: str):
    label = route(question)
    with tracer.start_span("router.dispatch", attributes={"label": label}):
        # BUG: sloppy parsing flips labels if text contains both words
        # e.g., "Is our TECH budget approved?" triggers both tokens in parsing.
        if re.search(r"TECH.*FINANCE|FINANCE.*TECH", label):
            label = "TECH" if "FINANCE" in label else "FINANCE"  # nonsense flip
        target = "FinanceBot" if label.startswith("FIN") else "TechBot"
        return f"[{target}] Answer to: {question}"

if __name__ == "__main__":
    print(handle("Is our TECH budget approved for Q4?"))
