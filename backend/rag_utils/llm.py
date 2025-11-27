# rag_utils/llm.py
import subprocess
import json

def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to Ollama llama3 in one-shot mode and returns the output text.
    """
    try:
        # Ollama expects a single JSON payload for non-interactive run
        payload = json.dumps({"prompt": prompt})

        result = subprocess.run(
            ["ollama", "run", "llama3"],  # one-shot run
            input=payload,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error calling LLM: {e}\nOutput: {e.output}\nStderr: {e.stderr}"
