from . import views
from django.urls import path, re_path

app_name = "games_view"

urlpatterns = [
    re_path(
        r"^search/$",
        views.GamesSearchListView.as_view(),
        name='games_search'),
]