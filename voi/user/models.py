from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
# Create your models here.

def url_upload_to(instance, filename):
    name, ext = filename.split('.')
    filepath = f'user_avatar/user_{instance.user_id.id}/{name}-{uuid4()}.{ext}'
    return filepath

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=100, unique=True)
    user_activation_uuid = models.TextField()
    reset_password_uuid = models.TextField(null=True)
    
    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE)
    
    date_joinded = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    username = models.CharField(max_length=25)
    user_avatar = models.OneToOneField(
        'ImageProfile',
        on_delete=models.CASCADE,
        null=True)
    date_of_birth = models.DateTimeField()

class ImageProfile(models.Model):
    user_profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    file_url = models.FileField(upload_to=url_upload_to, default="user_avatar/base_avatar/test.png")