from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length = 10000)
