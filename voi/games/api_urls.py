from . import api_views
from django.urls import path, re_path

app_name = "games_api"

urlpatterns = [
    re_path(
        r"^search/$",
        api_views.GamesSearchList.as_view(),
        name='games_search'),

    path(
        "test",
        api_views.test.as_view(),
        name = "test"
        )
]