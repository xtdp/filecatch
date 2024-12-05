from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FileUpload
import os
from django.conf import settings
from datetime import datetime

@api_view(['POST'])
def upload_file(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
    file = request.FILES['file']
    user_id = request.data.get('user_id')

    if file.size > 5 * 1024 * 1024:
        return Response({"error": "File too large."}, status=status.HTTP_400_BAD_REQUEST)

    valid_file_types = ('.png', '.jpg', '.jpeg', '.pdf')
    if not file.name.endswith(valid_file_types):
        return Response({"error": "Invalid file type. Allowed types: png, jpg, jpeg, pdf."}, status=status.HTTP_400_BAD_REQUEST)

    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except Exception as e:
        return Response({"error": f"Failed to save file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    file_upload = FileUpload(
        user_id=user_id,
        filename=file.name,
        path=file_path,
        file_size=file.size,
        file_type=file.content_type,
        uploaded_at=datetime.now()
    )
    
    try:
        file_upload.save()
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response({"error": f"Failed to save file metadata: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "File uploaded successfully.", "file_id": file_upload.user_id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_files(request):
    files = FileUpload.objects.all()
    
    response_data = []
    for file in files:
        response_data.append({
            "user_id": file.user_id,
            "filename": file.filename,
            "path": file.path,
            "file_size": file.file_size,
            "file_type": file.file_type,
            "uploaded_at": file.uploaded_at.isoformat()
        })
    
    return Response(response_data)

@api_view(['DELETE'])
def delete_file(request, user_id):
    try:
        file_uploads = FileUpload.objects.filter(user_id=user_id)
        if not file_uploads.exists():
            return Response({"error": "No files found for this user."}, status=status.HTTP_404_NOT_FOUND)

        for file_upload in file_uploads:
            if os.path.exists(file_upload.path):
                os.remove(file_upload.path)
            
            file_upload.delete()

        return Response({"message": "Files deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)