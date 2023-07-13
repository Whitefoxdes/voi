from django.db import models
from uuid import uuid4
# Create your models here.

def url_upload_to_for_game(instance, filename):
    name, ext = filename.split('.')
    filepath = f'game_screenshot/game_{instance.game.id}/{name}-{uuid4()}.{ext}'
    return filepath

class Games(models.Model):
    name = models.TextField(unique=True)
    is_active = models.BooleanField(default=False)
    genere = models.ManyToManyField("GameGenere")
    def __str__(self):
        return self.name

class GameScreenshot(models.Model):
    game = models.ForeignKey("Games", related_name="screenshot", on_delete=models.CASCADE)
    file_url = models.FileField(upload_to=url_upload_to_for_game)
    is_delete = models.BooleanField(default=False)

class GameGenere(models.Model):
    genere_name = models.TextField()

    def __str__(self):
        return self.genere_name