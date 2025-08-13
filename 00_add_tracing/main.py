# main.py
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv; load_dotenv()

def main():
    endpoint = os.environ["MODEL_ENDPOINT"]
    key = os.environ["API_CREDENTIAL_TOKEN"]
    model = os.getenv("MODEL_NAME")  # optional in some setups

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("Explain the benefits of continuous integration in 3 bullet points.")
    ]

    response = client.complete(model=model, messages=messages)
    content = response.choices[0].message.content
    
    print(json.dumps({"summary": content.strip()}, indent=2))

if __name__ == "__main__":
    main()
