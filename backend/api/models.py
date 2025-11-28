# backend/api/models.py
from django.db import models
from django.contrib.postgres.fields import ArrayField


class DocumentEmbedding(models.Model):
    file_name = models.CharField(max_length=255)
    chunk_text = models.TextField()
    embedding = ArrayField(models.FloatField())  # store list of floats
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.created_at}"
