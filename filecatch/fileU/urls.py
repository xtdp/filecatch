from django.urls import path
from .views import upload_file, list_files, delete_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('uploads/', list_files, name='list_files'),
    path('uploads/<str:user_id>/', delete_file, name='delete_file'),
]