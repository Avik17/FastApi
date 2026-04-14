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

