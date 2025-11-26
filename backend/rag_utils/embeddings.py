import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

def get_embedding(text: str):
    """
    Returns a vector embedding for the given text using Ollama's embedding model.
    """
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )

    data = response.json()

    if "embedding" not in data:
        raise ValueError(f"Embedding failed: {data}")

    return data["embedding"]
