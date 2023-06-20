from . import api_views
from django.urls import path, re_path

app_name = "games_api"

urlpatterns = [
    re_path(
        r"^search/$",
        api_views.GamesSearchList.as_view(),
        name='games_search'
    ),

    path(
        "add-game",
        api_views.AddGame.as_view(),
        name="add_game"
    ),

    path(
        "upload-screenshot-for-game/<int:game_id>",
        api_views.ScreenshotForGameUpload.as_view(),
        name="screenshot_upload"
    )
]