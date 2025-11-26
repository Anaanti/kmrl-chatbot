import os
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from PyPDF2 import PdfReader

from .models import Document
from .serializers import DocumentSerializer
from django.http import JsonResponse
from .models import DocumentChunk
from .embeddings import get_embedding

def test_pgvector(request):
    text = "This is a test sentence for embeddings."
    emb = get_embedding(text)

    obj = DocumentChunk.objects.create(
        chunk_text=text,
        embedding=emb
    )

    return JsonResponse({"saved_id": obj.id})


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_document(request):
    try:
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded"}, status=400)

        # Save file to media root
        save_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        with open(save_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Extract text
        extracted_text = extract_text_from_pdf(save_path)

        # Save Document entry
        doc = Document.objects.create(
            title=uploaded_file.name,
            file=uploaded_file,
        )

        return Response({
            "message": "Uploaded successfully",
            "document_id": doc.id,
            "extracted_text_preview": extracted_text[:300]
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)
