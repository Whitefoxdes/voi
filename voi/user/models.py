from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils import timezone
# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=25)
    email = models.EmailField(verbose_name="email",max_length=100, unique=True)
    date_of_birth = models.DateTimeField()
    date_joinded = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'