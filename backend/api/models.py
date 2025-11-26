from django.db import models
from pgvector.djmodels import VectorField


class Document(models.Model):
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    chunk_text = models.TextField()
    embedding = VectorField(dim=768)  # Ollama default embedding size

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk of {self.document.file.name}"
