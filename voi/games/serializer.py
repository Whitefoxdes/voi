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
        child = serializers.FileField(write_only=True)
    )

class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = [
            "name",
            "screenshot"
        ]
    name = serializers.CharField()
    screenshot = GameScreeonshotSerializer(many=True, required=False)