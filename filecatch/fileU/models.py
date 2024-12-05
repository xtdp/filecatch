from djongo import models

class FileUpload(models.Model):
    user_id = models.CharField(max_length=255, primary_key=True)
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    file_type = models.CharField(max_length=50)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FileU'

    def __str__(self):
        return self.filename