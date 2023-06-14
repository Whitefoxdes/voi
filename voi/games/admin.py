from .models import Games,GameScreenshot
from django.contrib import admin
# Register your models here.

class GameScreenshotInline(admin.StackedInline):
    model = GameScreenshot
    extra = 5

class GamesAdmine(admin.ModelAdmin):
    inlines = [
        GameScreenshotInline
    ]

admin.site.register(Games, GamesAdmine)
