# main.py
import os
import json
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

def main():
    endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
    key = os.environ["AZURE_AI_CHAT_KEY"]
    model = os.getenv("MODEL_NAME")  # optional in some setups

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    messages = [
        SystemMessage("You are a helpful assistant."),
        UserMessage("Explain the benefits of continuous integration in 3 bullet points.")
    ]

    response = client.complete(model=model, messages=messages)
    text = response.choices[0].message.content[0].text
    print(json.dumps({"summary": text.strip()}, indent=2))

if __name__ == "__main__":
    main()
