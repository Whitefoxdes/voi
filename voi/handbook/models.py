from uuid import uuid4
from django.db import models
from user.models import User
from games.models import Games
# Create your models here.

def url_upload_to_for_handbook(instance, filename):
    name, ext = filename.split('.')
    filepath = f'handbook_screenshot/handbook_{instance.handbook.id}/{name}-{uuid4()}.{ext}'
    return filepath

class Handbook(models.Model):
    title = models.TextField(max_length=100)
    body = models.TextField(max_length=4000)
    type = models.ForeignKey("HandbookType", related_name="type", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="handbook", on_delete=models.CASCADE)
    game = models.ForeignKey(Games, related_name="handbook", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class HandbookType(models.Model):
    type_name = models.TextField()
    def __str__(self):
        return self.type_name

class HandbookScreenshot(models.Model):
    handbook = models.ForeignKey("Handbook", related_name="screenshot", on_delete=models.CASCADE)
    file_url = models.FileField(upload_to=url_upload_to_for_handbook)