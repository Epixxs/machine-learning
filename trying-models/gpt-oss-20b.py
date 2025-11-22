import os
from openai import OpenAI
os.environ["HF_TOKEN"] = ""

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

querry = str(input("Enter your querry: "))

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b:groq",
    messages=[
        {
            "role": "user",
            "content": querry
        }
    ],
)

print(completion.choices[0].message)