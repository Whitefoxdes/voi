from .models import (
    Handbook,
    HandbookType,
    HandbookScreenshot
)
from rest_framework import serializers
from user.serializer import UserSerializer
from games.serializer import GamesSerializer

class HandbookScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandbookScreenshot
        fields = [
            "id",
            "file_url"
        ]
    file_url = serializers.ListField(
        child = serializers.FileField(write_only=True),
    )
    id = serializers.ListField(
        child = serializers.IntegerField(required=False),
        required=False
    )

class HandbookScreenshotURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandbookScreenshot
        fields = [
            "id",
            "file_url",
            "is_delete"
        ]
    id = serializers.CharField(required=False)
    file_url = serializers.URLField()
    is_delete = serializers.BooleanField(required=False)

class HandbookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandbookType
        fields = [
            "id",
            "type_name"
        ]
    id = serializers.IntegerField(required=False)
    type_name = serializers.CharField()

class HandbookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Handbook
        fields = [
            "id",
            "type",
            "body",
            "game",
            "title",
            "author",
            "screenshot"
        ]
    id = serializers.IntegerField(required=False)
    type = HandbookTypeSerializer()
    body = serializers.CharField()
    title= serializers.CharField()
    screenshot = HandbookScreenshotURLSerializer(
        many=True,
        required=False
        )
    author = UserSerializer(required=False)
    game = GamesSerializer(required=False)