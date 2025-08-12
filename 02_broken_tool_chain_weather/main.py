import os
import json
import re
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage, UserMessage,
    ChatCompletionsToolDefinition, FunctionDefinition
)
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

# Initialize tracing
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

@tracer.start_as_current_span("scenario_02")
def run(query: str):
    current_span = trace.get_current_span()
    current_span.set_attribute("scenario.name", "broken_tool_chain_weather")
    current_span.set_attribute("query", query)
    
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
    with tracer.start_span("process_tool_calls") as tool_span:
        tool_span.set_attribute("tool_calls_count", len(tool_calls))
        for tc in tool_calls:
            if tc.function and tc.function.name == "get_weather":
                # Extract the city with a sloppy regex (bug) that rejects spaces
                m = re.search(r'"city"\s*:\s*"([A-Za-z]+)"', tc.function.arguments or "")
                if not m:
                    # silently skip (the bug) instead of handling properly
                    tool_span.set_attribute("bug_triggered", True)
                    continue
                result = fake_weather(m.group(1))
                tool_outputs.append({"tool_call_id": tc.id, "output": result})
        tool_span.set_attribute("successful_tool_calls", len(tool_outputs))

    # Send tool results (maybe missing because of the bug)
    follow = client.complete(
        model=MODEL,
        messages=[*messages, msg],
        tool_results=tool_outputs
    )
    
    content = follow.choices[0].message.content
    
    # Handle both string and list content formats
    text_content = content if isinstance(content, str) else (
        content[0].text if hasattr(content[0], 'text') else str(content[0])
    )
    
    # Add choice event
    add_choice_event(current_span, content)
    
    return text_content

if __name__ == "__main__":
    print(run("What's the weather in New York?"))
