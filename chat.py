import os,anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import List

load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
app=FastAPI()

class Message(BaseModel):
    role:str
    content:str

class chatRequest(BaseModel):
    message:str
    history:List[Message]

class chatResponse(BaseModel):
    reply:str
    history:List[Message]
    input_tokens:int
    output_tokens:int
MAX_HISTORY=10

@app.post("/chat",response_model=chatResponse)
async def chat(request:chatRequest):
        messages=[m.model_dump() for m in request.history]
        messages.append({"role":"user","content":request.message})
        if len(messages>MAX_HISTORY):
             messages=messages[-MAX_HISTORY]
        response=client.messages.create(max_tokens=1024,
                                     messages=messages,
                                     model="claude-haiku-4-5-20251001",
                                     system="You are s senior Software enhineer at Google")
        
        reply= response.content[0].text
        messages.append({"role": "assistant", "content": reply})

        return {
        "reply": reply,
        "history": messages,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }