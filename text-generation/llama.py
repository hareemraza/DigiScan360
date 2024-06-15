import os
from typing import List, Dict

from groq import Groq
import requests

# Groq API key
os.environ["GROQ_API_KEY"] = ""

LLAMA3_8B_INSTRUCT = "llama3-8b-8192"
DEFAULT_MODEL = LLAMA3_8B_INSTRUCT

client = Groq()


def assistant(content: str):
    return {"role": "assistant", "content": content}


def user(content: str):
    return {"role": "user", "content": content}


def chat_completion(
    messages: List[Dict],
    model=DEFAULT_MODEL,
    temperature: float = 0.4,
    top_p: float = 0.9,
) -> str:
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].message.content


def llama3(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.4,
    top_p: float = 0.9,
) -> str:
    return chat_completion(
        [user(prompt)],
        model=model,
        temperature=temperature,
        top_p=top_p,
    )


def ollama(prompt):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "llama3",
        "messages": [
            {
              "role": "user",
              "content": prompt
            }
        ],
        "stream": False
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    return(response.json()['message']['content'])