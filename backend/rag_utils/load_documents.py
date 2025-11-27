# rag_utils/load_documents.py
import os
from rag_utils.chunker import chunk_text
from rag_utils.embedder import embed_text
from rag_utils.embeddings_store import store_embedding

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
BASE_DIR = os.path.dirname(BASE_DIR) 

FOLDER = os.path.join(BASE_DIR, "docs")

def load_txt_files():
    for fname in os.listdir(FOLDER):
        if fname.endswith(".txt"):
            path = os.path.join(FOLDER, fname)
            text = open(path, "r", encoding="utf-8").read()
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                emb = embed_text(chunk)
                store_embedding(f"{fname}_chunk{i}", chunk, emb)
                print("Inserted:", fname, "chunk", i)

if __name__ == "__main__":
    load_txt_files()
