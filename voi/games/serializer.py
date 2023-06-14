from .models import (
    Games, GameScreenshot
)

from rest_framework import serializers

class GameScreeonshoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScreenshot
        fields = [
            "file_url"
        ]
    # file_url = serializers.CharField()
    file_url = serializers.URLField()

class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = [
            "name",
            "screenshot"
        ]
    name = serializers.CharField()
    screenshot = GameScreeonshoSerializer(many=True)
