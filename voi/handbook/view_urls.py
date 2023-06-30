from . import views
from django.urls import path, re_path

app_name = "handbook_view"

urlpatterns = [
    path(
        "create-handbook-for-game/<int:game_id>",
        views.CreateHandbookView.as_view(),
        name='create_handbook'
    )
]