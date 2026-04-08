import gradio as gr
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MAX_HISTORY=10

def chat(message,history):
    messages=[]
     # convert Gradio history format to Anthropic format
    for item in history:
        messages.append({
            "role": item["role"],
            "content": item["content"]
        })

    messages.append({"role":"user","content":message})    
    if len(messages) > MAX_HISTORY:
         messages=messages[-MAX_HISTORY:]
    response=client.messages.create(max_tokens=1024,
                                    messages=messages,
                                    model="claude-haiku-4-5-20251001",
                                    system="You are a helpful AI Engineering assistant. Help users learn AI Engineering concepts and build projects.")
        
    return response.content[0].text

# build the UI
demo = gr.ChatInterface(
    fn=chat,
    title="AI Engineering Assistant",
    description="Ask me anything about AI Engineering — LLMs, RAG, FastAPI, agents, deployment.",
    examples=[
        "What is RAG and when should I use it?",
        "Explain the difference between async def and def in FastAPI",
        "How do I reduce LLM API costs in production?"
    ]
)

demo.launch(share=True)