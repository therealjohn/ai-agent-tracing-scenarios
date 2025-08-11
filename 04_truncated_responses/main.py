import os, json
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

init_tracing("scenario04")
tracer = get_tracer("scenario04")
client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

if __name__ == "__main__":
    messages = [
        SystemMessage("You write detailed summaries of 400-600 words."),
        UserMessage("Summarize the benefits of CI/CD and trunk-based development.")
    ]
    # Intentionally low output tokens to trigger length truncation
    resp = client.complete(model=MODEL, messages=messages, max_output_tokens=50)
    choice = resp.choices[0]
    
    content = choice.message.content
    # Handle both string and list content formats
    if isinstance(content, str):
        text = content
    else:
        # If content is a list, get the text from the first item
        text = content[0].text if hasattr(content[0], 'text') else str(content[0])
    
    print(json.dumps({
        "finish_reason": getattr(choice, "finish_reason", "unknown"),
        "text": text
    }, indent=2))
