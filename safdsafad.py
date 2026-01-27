#import os
#from openai import OpenAI
#from pathlib import Path
#from dotenv import load_dotenv
#
#load_dotenv()
#API_KEY = os.getenv("HF_TOKEN")
#
#client = OpenAI(
#    base_url="https://router.huggingface.co/v1",
#    api_key=API_KEY,
#)
#
#
#
#completion = client.chat.completions.create(
#    model="meta-llama/Llama-3.1-8B-Instruct:novita",
#    messages=[
#        {
#            "role": "user",
#            "content": "What is the capital of France?"
#        }
#    ],
#)
#
#print(completion.choices[0].message)


import os
import requests
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("XAI_API_KEY")

if not API_KEY:
    raise RuntimeError("Falta la variable de entorno OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

response = requests.post(
    URL,
    headers=headers,
    json={
        "model": "x-ai/grok-4.1-fast",
        "messages": [
            {"role": "user", "content": "How many r's are in the word 'strawberry'?"}
        ]
    }
)

print(response.status_code)
print(response.text)
