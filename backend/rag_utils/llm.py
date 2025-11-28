import subprocess
import random
import json

# ---------------------------
# LLM function (CLI-based)
# ---------------------------
def ask_llm(prompt: str) -> str:
    payload = json.dumps({"prompt": prompt})
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8"       # <- explicitly set UTF-8
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error calling LLM: {e}\nOutput: {e.output}\nStderr: {e.stderr}"

# ---------------------------
# Mock embedding function
# ---------------------------
def get_embedding(text: str) -> list:
    """
    Returns a dummy 384-dimensional vector for testing / ingestion.
    This allows RAG pipeline to run without a server.
    Later, you can replace this with real embeddings if needed.
    """
    return [random.random() for _ in range(384)]

# ---------------------------
# Optional quick test
# ---------------------------
if __name__ == "__main__":
    print("LLM output:", ask_llm("What is KMRL?"))
    print("Embedding length:", len(get_embedding("Hello world")))
