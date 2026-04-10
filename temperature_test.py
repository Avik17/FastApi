import os,anthropic
from dotenv import load_dotenv
load_dotenv()

client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = "Complete this sentence in exactly 10 words: The future of AI engineering is"

print("------Temperature:0.0-----")
for i in range(3):
    response=client.messages.create(max_tokens=100,temperature=0.0,
                                    model="claude-haiku-4-5-20251001",
                                    messages=[{"role":"user","content":prompt}])
    print(f"Run:{i+1}-{response.content[0].text.strip()}")

print("------Temperature:1.0-----")
for i in range(3):
    response=client.messages.create(max_tokens=100,temperature=1.0,
                                    model="claude-haiku-4-5-20251001",
                                    messages=[{"role":"user","content":prompt}])
    print(f"Run:{i+1}-{response.content[0].text.strip()}")

# Check how many tokens a long system prompt uses
long_system = "You are an AI assistant. " * 1000  # very long system prompt

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=10,
    system=long_system,
    messages=[{"role": "user", "content": "Hi"}]
)
print(f"Tokens used with long system prompt: {response.usage.input_tokens}")    