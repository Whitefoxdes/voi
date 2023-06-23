from . import views
from django.urls import path, re_path

app_name = "games_view"

urlpatterns = [
    re_path(
        r"^search/$",
        views.GamesSearchListView.as_view(),
        name='games_search'),

    path(
        "add-new-game",
        views.AddNewGame.as_view(),
        name='add_new_game'
    ),
    re_path(
        r"^all-games/$",
        views.AllGamesListView.as_view(),
        name='all_games'
    ),
    path(
        "<int:game_id>",
        views.GameInfo.as_view(),
        name='game_info'
    )
]