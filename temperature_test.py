import os,anthropic
from dotenv import load_dotenv
load_dotenv()

client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt="Explain AI Engineering in 10 Sentences"


for i in range(3):
    response=client.messages.create(max_tokens=100,temperature=0.0,
                                    model="claude-haiku-4-5-20251001",messages=[{"role":"user","content":prompt}])
    print(f"{response.content[0].text.strip()}")

print("="*20)
for i in range(3):
    response=client.messages.create(max_tokens=100,temperature=1.0,
                                    model="claude-haiku-4-5-20251001",messages=[{"role":"user","content":prompt}]),
    print(f"{response.content[0].text.strip()}")