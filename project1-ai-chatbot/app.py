import gradio as gr
import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MAX_HISTORY = 10
total_input_tokens = 0
total_output_tokens = 0
DAILY_BUDGET = 10000  # tokens

# ─── Tool definitions ─────────────────────────────────────
tools = [
    {
        "name": "get_time",
        "description": "Get the current date and time",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "calculate",
        "description": "Perform a mathematical calculation. Use for any arithmetic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression e.g. '2 + 2'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city"
                }
            },
            "required": ["city"]
        }
    }
]

# ─── Tool functions ───────────────────────────────────────
def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def calculate(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather(city: str):
    weather_data = {
        "patna":     "32°C, Sunny",
        "delhi":     "28°C, Hazy",
        "mumbai":    "30°C, Humid",
        "bangalore": "24°C, Cloudy"
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")

def run_tool(tool_name: str, tool_input: dict):
    if tool_name == "get_time":
        return get_time()
    elif tool_name == "calculate":
        return calculate(tool_input["expression"])
    elif tool_name == "get_weather":
        return get_weather(tool_input["city"])
    else:
        return f"Unknown tool: {tool_name}"

def chat(message, history):
    global total_input_tokens, total_output_tokens
    
    # Check budget before calling API
    if total_input_tokens + total_output_tokens > DAILY_BUDGET:
        return "Daily token budget exceeded. Please try again tomorrow."
    
    messages = []

    # Gradio 6.x history — list of dicts with role, content, metadata
    for item in history:
        role = item.get("role")
        content = item.get("content")
        # Only pass clean text messages to Claude — skip tool blocks
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})

    if len(messages) > MAX_HISTORY:
        messages = messages[-MAX_HISTORY:]

    # Separate working copy for tool loop
    working_messages = list(messages)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="""You have tools to get the time, calculate math, and check weather.
IMPORTANT: When you answer using a tool result, remember that you DID use that tool. 
If asked follow-up questions about a previous calculation or result, acknowledge that 
you calculated or retrieved it using your tools.""",
        tools=tools,
        messages=working_messages
    )

    while response.stop_reason == "tool_use":
        tool_use_block = next(
            block for block in response.content
            if block.type == "tool_use"
        )
        tool_name   = tool_use_block.name
        tool_input  = tool_use_block.input
        tool_use_id = tool_use_block.id

        tool_result = run_tool(tool_name, tool_input)

        working_messages.append({"role": "assistant", "content": response.content})
        working_messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": tool_result
            }]
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system="You are a helpful AI Engineering assistant.",
            tools=tools,
            messages=working_messages
        )
        total_input_tokens += response.usage.input_tokens
        total_output_tokens += response.usage.output_tokens
        final = next(
        block.text for block in response.content
        if hasattr(block, "text")
    )
    return final


# Gradio 6.12.0 — no type parameter needed, it's the default
demo = gr.ChatInterface(
    fn=chat,
    title="AI Engineering Assistant",
    description="Ask me anything about AI Engineering. I can also tell you the time, do calculations, and check weather for Indian cities.",
    examples=[
        "What time is it right now?",
        "What is 1234 multiplied by 5678?",
        "What is the weather in Patna?",
        "What is RAG and when should I use it?"
    ]
)


demo.launch(share=True)