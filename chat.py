import os,anthropic
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import List,Optional

load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
app=FastAPI()

class Message(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    message:str
    history:Optional[List[Message]]=[]

class ChatResponse(BaseModel):
    reply:str
    history:List[Message]
    input_tokens:int
    output_tokens:int
MAX_HISTORY=10

@app.post("/chat",response_model=ChatResponse)
async def chat(request:ChatRequest):
        messages=[m.model_dump() for m in request.history]
        messages.append({"role":"user","content":request.message})
        if len(messages)>MAX_HISTORY:
            messages=messages[-MAX_HISTORY:]
        response=client.messages.create(max_tokens=1024,
                                     messages=messages,
                                     model="claude-haiku-4-5-20251001",
                                     system="You are Senior Software engineer at Google")
        
        reply= response.content[0].text
        messages.append({"role": "assistant", "content": reply})

        return {
        "reply": reply,
        "history": messages,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }

@app.post("/chat/stream")
async def chat_stream(request:ChatRequest):
        messages=[m.model_dump() for m in request.history]
        messages.append({"role":"user","content":request.message})
        if len(messages)>MAX_HISTORY:
            messages=messages[-MAX_HISTORY:]
        def generate():
            with client.messages.stream(max_tokens=1024,
                                     messages=messages,
                                     model="claude-haiku-4-5-20251001",
                                     system="You are s senior Software enhineer at Google") as stream:
                 for text in stream.text_stream:
                    yield text

        return StreamingResponse(generate(), media_type="text/plain")