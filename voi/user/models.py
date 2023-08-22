from uuid import uuid4
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    PermissionsMixin,
    AbstractBaseUser,
)
from django.core.validators import FileExtensionValidator

def url_upload_to_for_user_avatar(instance, filename):
    name, ext = filename.split('.')
    dir_path = f'user_avatar/user_{instance.user_profile.id}'
    filepath = f'{dir_path}/{name}-{uuid4()}.{ext}'
    return filepath

# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=25)
    user_avatar = models.OneToOneField(
        'ImageProfile',
        on_delete=models.CASCADE,
        null=True
    )
    date_of_birth = models.DateField()

class UserManager(BaseUserManager):

    def create_user(self, email, password):

        if email is None:
            raise TypeError('Users must have an email address.')

        profile = Profile(
            username = "superuser",
            date_of_birth = "2000-01-01")

        profile.save()

        user = self.model(
            email=self.normalize_email(email),
            profile=profile)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            email,
            password
        )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email",
        max_length=100,
        unique=True)
    user_activation_uuid = models.TextField()
    reset_password_uuid = models.TextField(null=True)
    profile = models.OneToOneField(
        "Profile",
        on_delete=models.CASCADE
    )
    date_joinded = models.DateTimeField(
        verbose_name="date joined",
        auto_now_add=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class ImageProfile(models.Model):
    user_profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE)
    file_url = models.FileField(upload_to=url_upload_to_for_user_avatar)