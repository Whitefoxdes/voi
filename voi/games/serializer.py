from .models import (
    Games, GameScreenshot
)

from rest_framework import serializers

class GameScreeonshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScreenshot
        fields = [
            "file_url"
        ]
    file_url = serializers.ListField(
        child = serializers.FileField(write_only=True),
    )

class GameScreeonshotURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScreenshot
        fields = [
            "file_url",
        ]
    file_url = serializers.URLField()

class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = [
            "id",
            "name",
            "screenshot"
        ]
    name = serializers.CharField()
    id = serializers.IntegerField(required=False)
    screenshot = GameScreeonshotURLSerializer(many=True, required=False)