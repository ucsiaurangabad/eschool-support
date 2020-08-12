from django.db import models

# class ProfileImage(models.Model):
#     image = models.FileField()
    
from crud.storage_backends import PublicMediaStorage


class ProfileImage(models.Model):
    uploaded_at = models.DateTimeField(auto_now=True)
    file = models.FileField(storage=PublicMediaStorage())