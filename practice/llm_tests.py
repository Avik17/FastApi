import anthropic,os
from dotenv import load_dotenv

load_dotenv()


client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
messages=[]

while True:
    user_input=input("Chat with Claude (type 'quit' to exit)\n")
    if user_input.lower()=="quit":
        break


    messages.append(
            {"role": "user", "content": user_input}
              )
    response = client.messages.create(
    max_tokens=1024,
    messages=messages,
    model="claude-haiku-4-5-20251001",
    system="You are a helpful AI engineering assistant.")
    claude_reply=response.content[0].text
    messages.append({"role":"assistant","content":claude_reply})
    print(claude_reply)
    print("---")
    print(f"Input tokens:  {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")
    print(f"Total tokens:  {response.usage.input_tokens + response.usage.output_tokens}")
        

# Cost calculation — Haiku pricing
    input_cost  = (response.usage.input_tokens / 1_000_000) * 0.80
    output_cost = (response.usage.output_tokens / 1_000_000) * 4.00
    total_cost  = input_cost + output_cost

print(f"\nCost this call: ${total_cost:.6f}")
print(f"Cost per 1000 calls like this: ${total_cost * 1000:.4f}")
print(f"Cost per 10000 calls like this: ${total_cost * 10000:.4f}")