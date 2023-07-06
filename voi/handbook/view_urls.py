from . import views
from django.urls import path, re_path

app_name = "handbook_view"

urlpatterns = [
    path(
        "create/<int:game_id>",
        views.CreateHandbookView.as_view(),
        name='create_handbook'
    ),
    re_path(
        r"handbook-list/$",
        views.AllHandbookListView.as_view(),
        name='all_handbook_list'
    ),
    path(
        "<int:handbook_id>",
        views.HandbookInfoView.as_view()
    ),
    path(
        "edit/<int:handbook_id>",
        views.EditHandbookView.as_view()
    )
]