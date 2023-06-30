from . import api_views
from django.urls import path, re_path

app_name = "handbook_api"

urlpatterns = [
    path(
        "create-handbook-for-game/<int:game_id>",
        api_views.CreateHandbook.as_view(),
        name='create_handbook'
    ),
    path(
        "handbook-type-list",
        api_views.HandbookTypeList.as_view(),
    ),
    path(
        "upload-screenshot-for-handbook/<int:handbook_id>",
        api_views.ScreenshotUpload.as_view(),
    ),
]