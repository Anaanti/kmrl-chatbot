from sentence_transformers import SentenceTransformer

# Load model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    """
    Returns a real embedding vector using SentenceTransformer.
    Converts the result to a Python list for PostgreSQL ArrayField.
    """
    vec = embedding_model.encode(text)  # returns a numpy array
    return vec.tolist()