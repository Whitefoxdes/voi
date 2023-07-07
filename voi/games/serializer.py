from .models import (
    Games,
    GameGenere,
    GameScreenshot
)

from rest_framework import serializers

class GameScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScreenshot
        fields = [
            "file_url"
        ]
    file_url = serializers.ListField(
        child = serializers.FileField(write_only=True),
    )

class GameScreenshotURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScreenshot
        fields = [
            "file_url",
        ]
    file_url = serializers.URLField()

class GameGenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenere
        fields = [
            "id",
            "genere_name"
        ]
    id = serializers.IntegerField(required=False)
    genere_name = serializers.CharField()

class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = [
            "id",
            "name",
            "genere",
            "screenshot"
        ]
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    genere = GameGenereSerializer(many=True, required=False)
    screenshot = GameScreenshotURLSerializer(many=True, required=False)
