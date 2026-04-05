import anthropic,os
from dotenv import load_dotenv

load_dotenv()
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message=client.messages.create(model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role":"user","content":"What is AI engineering? Explain in 3 sentences."}])
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is RAG in AI engineering? Explain in 3 sentences."}
    ]
)

print(message.content[0].text)
print("---")
print(f"Input tokens:  {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
print(f"Total tokens:  {message.usage.input_tokens + message.usage.output_tokens}")

# Cost calculation — Haiku pricing
input_cost  = (message.usage.input_tokens / 1_000_000) * 0.80
output_cost = (message.usage.output_tokens / 1_000_000) * 4.00
total_cost  = input_cost + output_cost

print(f"\nCost this call: ${total_cost:.6f}")
print(f"Cost per 1000 calls like this: ${total_cost * 1000:.4f}")
print(f"Cost per 10000 calls like this: ${total_cost * 10000:.4f}")