from django.contrib import admin
from .models import (
    Handbook,
    HandbookType,
    HandbookScreenshot
    )

# Register your models here.


class HandbookScreenshotInline(admin.StackedInline):
    model = HandbookScreenshot
    extra = 15

class HandbookAdmine(admin.ModelAdmin):
    inlines = [
        HandbookScreenshotInline        
    ]

admin.site.register(Handbook, HandbookAdmine)
admin.site.register(HandbookType)