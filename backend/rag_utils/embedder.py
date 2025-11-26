from embeddings import Embeddings  # your embeddings.py

class Embedder:
    def __init__(self):
        self.embedder = Embeddings()

    def embed_texts(self, texts: list):
        return [self.embedder.get_embedding(text) for text in texts]
