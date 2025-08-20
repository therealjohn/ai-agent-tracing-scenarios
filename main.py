import os
import json
import re
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage, UserMessage, ToolMessage,
    ChatCompletionsToolDefinition, FunctionDefinition
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from opentelemetry import trace

# Load environment and setup path
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _shared.tracing import add_choice_event, add_gen_ai_event, init_tracing, get_tracer
import argparse

# Configuration
ENDPOINT = os.environ["MODEL_ENDPOINT"]
KEY = os.environ["API_CREDENTIAL_TOKEN"]
MODEL = os.getenv("MODEL_NAME")

# Initialize tracing
init_tracing("scenario03")
tracer = get_tracer("scenario03")
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
    return json.dumps({"city": city, "temp_c": 27})

@tracer.start_as_current_span("scenario_03")
def run(query: str):
    current_span = trace.get_current_span()
    
    messages = [
        SystemMessage("You must ALWAYS call get_weather and include its result."),
        UserMessage(query),
    ]

    # Add user message event
    add_gen_ai_event(current_span, "gen_ai.user.message", "user", query)

    # Ask the model with a tool definition
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
                # Still need to provide a response to avoid API error
                tool_outputs.append({"tool_call_id": tc.id, "output": "Error: Unable to process city name"})
                continue
            result = fake_weather(m.group(1))
            tool_outputs.append({"tool_call_id": tc.id, "output": result})

    # Send tool results (maybe missing because of the bug)
    # Add tool results as ToolMessage objects to the messages
    messages_with_tools = [*messages, msg]
    for tool_output in tool_outputs:
        messages_with_tools.append(
            ToolMessage(content=tool_output["output"], tool_call_id=tool_output["tool_call_id"])
        )
    
    follow = client.complete(
        model=MODEL,
        messages=messages_with_tools
    )
    
    content = follow.choices[0].message.content

    # Add choice event
    add_choice_event(current_span, content)
    current_span.set_attribute("gen_ai.usage.total_tokens", follow.usage.total_tokens)
    return str(content)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Get weather information for a city")
    parser.add_argument("city", nargs="?", default="New York", help="City to get weather for (default: New York)")
    args = parser.parse_args()
    
    print(run(f"What's the weather in {args.city}?"))
