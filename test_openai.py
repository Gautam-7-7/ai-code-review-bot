import os
from openai import OpenAI

# get your key from env variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ No OPENAI_API_KEY found in environment")
    exit(1)

print("✅ OpenAI key detected, testing request...")

client = OpenAI(api_key=api_key)

# simple test: ask GPT something
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": "Say hello in one short sentence."}
    ]
)

print("GPT says:", response.choices[0].message.content)
