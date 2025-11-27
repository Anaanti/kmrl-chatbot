import ollama

def query_llm(prompt: str) -> str:
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

client = Client(host=OLLAMA_HOST)

def query_llm(prompt: str) -> str:
    """Query Llama3 using Ollama."""
    response = client.generate(
        model=LLM_MODEL,
        prompt=prompt
    )
    return response["response"]
