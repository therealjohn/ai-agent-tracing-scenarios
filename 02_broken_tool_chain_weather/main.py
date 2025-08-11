import os, json, re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage, UserMessage,
    ChatCompletionsToolDefinition, FunctionDefinition
)
from azure.core.credentials import AzureKeyCredential
from pathlib import Path
import sys

from dotenv import load_dotenv; load_dotenv()

sys.path.append(str(Path(__file__).resolve().parents[1] / "_shared"))
from tracing import init_tracing, get_tracer

ENDPOINT = os.environ["AZURE_AI_CHAT_ENDPOINT"]
KEY = os.environ["AZURE_AI_CHAT_KEY"]
MODEL = os.getenv("MODEL_NAME")

init_tracing("scenario02")
tracer = get_tracer("scenario02")

client = ChatCompletionsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

# Define a simple tool (function) schema
weather_tool = ChatCompletionsToolDefinition(
    function=FunctionDefinition(
        name="get_weather",
        description="Get current Celsius temperature for a given city",
        parameters={
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    )
)

def fake_weather(city: str) -> str:
    with tracer.start_span("tool.get_weather"):
        return json.dumps({"city": city, "temp_c": 27})

def run(query: str):
    messages = [
        SystemMessage("You must ALWAYS call get_weather and include its result."),
        UserMessage(query),
    ]

    # Ask the model with a tool definition (tool call will come back in the response)
    first = client.complete(model=MODEL, messages=messages, tools=[weather_tool])

    msg = first.choices[0].message
    tool_calls = getattr(msg, "tool_calls", []) or []

    # BUG: we 'ignore' tool calls if city has a space (e.g., 'New York')
    tool_outputs = []
    for tc in tool_calls:
        if tc.function and tc.function.name == "get_weather":
            # Extract the city with a sloppy regex (bug) that rejects spaces
            m = re.search(r'"city"\s*:\s*"([A-Za-z]+)"', tc.function.arguments or "")
            if not m:
                # silently skip (the bug) instead of handling properly
                continue
            result = fake_weather(m.group(1))
            tool_outputs.append({"tool_call_id": tc.id, "output": result})

    # Send tool results (maybe missing because of the bug)
    follow = client.complete(
        model=MODEL,
        messages=[*messages, msg],
        tool_results=tool_outputs
    )
    
    content = follow.choices[0].message.content
    
    # Handle both string and list content formats
    if isinstance(content, str):
        return content
    else:
        # If content is a list, get the text from the first item
        return content[0].text if hasattr(content[0], 'text') else str(content[0])

if __name__ == "__main__":
    print(run("What's the weather in New York?"))
