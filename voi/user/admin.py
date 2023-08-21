from .models import (
    User,
    Profile,
    ImageProfile
)
from django.contrib import admin

# Register your models here.

class ImageProfileInline(admin.StackedInline):
    model = ImageProfile
    extra = 1

class ProfileAdmine(admin.ModelAdmin):
    inlines = [
        ImageProfileInline
    ]

admin.site.register(User)
admin.site.register(
    Profile,
    ProfileAdmine
    )