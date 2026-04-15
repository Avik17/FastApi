import anthropic
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools=[
    {
    "name":"get_time",
    "description":"Get the current date and time",
    "input_schema":{
        "type":"object",
        "properties":{},
        "required":[]

    }
},
{

"name":"calculate",
"description":"Perform a mathematical calculation.Use this for any arithmetic.",
"input_schema":{
    "type":"object",
    "properties":{
        "expression":{
            "type":"string",
            "description":"The mathematical expression to evaluate e.g '2+2'"
        }
        },

        "required":["expression"]
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
def get_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
def calculate(expression:str):
    try:
        result=eval(expression)
        return str(result)
    except Exception as e:
        return f"Error:{str(e)}"
    
def get_weather(city:str):
    weather_data={
        "patna":"32C ,Sunny",
        "delhi": "28 ,Hazy",
        "mumbai":"30C ,Humid",
        "bangalore":"24C ,Cloudy"
    }    
    return weather_data.get(city.lower(),f"Weather data not available for {city}")

def run_tool(tool_name:str,tool_input:dict):
    
    print(f"DEBUG: tool_name='{tool_name}' | tool_input={tool_input}")
    if tool_name=="get_time":
        return get_time()
    elif tool_name == "calculate":
        return calculate(tool_input["expression"])
    elif tool_name=="get_weather":
        return get_weather(tool_input['city'])
    else:
        return f"Unknown tool:{tool_name}"
    
def chat_with_tools(user_message:str):
    print(f"\nUser:{user_message}")
    messages=[{"role":"user","content":user_message}]

    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )    

    while response.stop_reason =="tool_use":
        tool_use_block=next(
            block for block in response.content
            if block.type=="tool_use"

        )
        tool_name=tool_use_block.name
        tool_input=tool_use_block.input
        tool_use_id=tool_use_block.id

        print(f"-> Claude calls:{tool_name}({tool_input})")

        tool_result=run_tool(tool_name=tool_name,tool_input=tool_input)
        print(f"-> Tool returned:{tool_result}")

        messages.append({"role":"assistant","content":response.content})
        messages.append({
            "role":"user",
            "content":[{
                "type": "tool_result",
                "tool_use_id":tool_use_id,
                "content":tool_result
            }]
        })

        response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        tools=tools,
        messages=messages)

    final=next(block.text for block in response.content
               if hasattr(block,"text")
         ) 
    print(f"Claude: {final}")
    return final


# ─── TEST ─────────────────────────────────────────────────
if __name__ == "__main__":
    chat_with_tools("What time is it right now?")
    chat_with_tools("What is 1234 multiplied by 5678?")
    chat_with_tools("What is the weather in Patna?")
    chat_with_tools("What is the weather in Tokyo?")   

