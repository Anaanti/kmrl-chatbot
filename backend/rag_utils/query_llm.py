# backend/rag_utils/query_llm.py

import os
from dotenv import load_dotenv
import psycopg2
from sentence_transformers import SentenceTransformer
from math import sqrt
from llama_cpp import Llama 

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# ---------------------------
# GLOBAL LLM VARIABLE for Lazy Loading
# ---------------------------
# Initialize to False, will be replaced by the Llama object when loaded
llm = False 

# ---------------------------
# LLM Initialization Function
# ---------------------------
def load_llm_model():
    """Initializes the LLM object only when called."""
    global llm

    # Path to the GGUF model file: kmrl-chatbot/backend/rag_utils/models/llama-3-8b.gguf
    MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models', 'llama-3-8b.gguf'))

    try:
        # n_gpu_layers=0 for CPU-only execution
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_gpu_layers=0, # Set to 0 for CPU-only
            verbose=False
        )
        print(f"Successfully loaded local LLM from: {MODEL_PATH}")
    except Exception as e:
        # Set to None if loading fails so we don't try again
        llm = None
        print(f"Error loading local LLM: {e}")
        print("Generation will fail. Check 'llama-cpp-python' installation and model path.")

# ---------------------------
# Postgres connection
# ---------------------------
def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ---------------------------
# LLM Generation Function
# ---------------------------
def generate_answer(prompt_template: str) -> str:
    """
    Calls the local LLaMA model via llama-cpp-python using the RAG prompt.
    """
    global llm
    
    # 1. Lazy Load Check: If LLM is not loaded (llm is False), try to load it now
    if llm is False:
        load_llm_model()
    
    if llm is None:
        return "LLM Generation Error: Local LLM failed to initialize."
    
    try:
        response = llm(
            prompt_template,
            max_tokens=512,
            # Use LLaMA chat formatting stop tokens for clean output
            stop=["<|eot_id|>", "<|end_of_text|>", "user:", "Question:"],
            temperature=0.1,
            echo=False,
        )
        # Extract the generated text
        answer = response['choices'][0]['text'].strip()
        return answer

    except Exception as e:
        print(f"LLM Generation Runtime Error: {e}")
        return f"LLM Generation Error during inference: {e}"


# ---------------------------
# Embedding model
# ---------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    return embed_model.encode(text).tolist()

# ---------------------------
# Euclidean distance
# ---------------------------
def euclidean(a, b):
    b = [float(x) for x in b]
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


# ---------------------------
# Query documents from DB
# ---------------------------
def query_documents(user_query, top_k=5):
    vec = get_embedding(user_query)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT doc_name, content, embeddings FROM document_embedding;")
    rows = cur.fetchall()
    results = []

    for doc_name, content, embeddings in rows:
        try:
            # Convert Postgres vector to list of floats
            if isinstance(embeddings, str):
                embeddings = [float(x) for x in embeddings.strip("[]").split(",")]
            dist = euclidean(vec, embeddings)
            results.append({"doc_name": doc_name, "content": content, "similarity": dist})
        except Exception as e:
            print(f"Skipping {doc_name} due to error: {e}")

    # Sort by smallest distance (closest match)
    results.sort(key=lambda x: x["similarity"])
    return results[:top_k]

# ---------------------------
# Get answer using LLM
# ---------------------------
def answer_query(user_query, top_k=5):
    top_docs = query_documents(user_query, top_k)
    context_str = "\n\n".join([doc['content'] for doc in top_docs])

    # RAG Prompt Template using LLaMA 3 ChatML format (Stricter for better answers)
    prompt_template = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an accurate assistant for the KMRL project.
Use ONLY the context provided in the CONTEXT section to answer the user's query.
If the answer is not in the context, state: "I cannot answer this based on the provided KMRL documents."
<|eot_id|><|start_header_id|>user<|end_header_id|>
CONTEXT:
---
{context_str}
---
QUERY: {user_query}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""
    # Call the new local generation function
    answer = generate_answer(prompt_template)

    # Constructing the expected output structure for the Django view
    return {"answer": answer, "sources": top_docs}

# ---------------------------
# Optional test block (__main__) MUST be REMOVED
# ---------------------------