from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'embedding', 'uploaded_at']
        read_only_fields = ['embedding', 'uploaded_at']
