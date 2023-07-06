from . import api_views
from django.urls import path, re_path

app_name = "handbook_api"

urlpatterns = [
    path(
        "create/<int:game_id>",
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
    re_path(
        r"handbook-list/$",
        api_views.AllHandbookList.as_view(),
    ),
    path(
        "<int:handbook_id>",
        api_views.HandbookInfo.as_view()
    ),
    path(
        "edit/<int:handbook_id>",
        api_views.EditHandbook.as_view()
    ),
    path(
        "delete/<int:handbook_id>",
        api_views.DeleteHandbook.as_view()
    ),
    path(
        "delete-screenshot/<int:handbook_id>",
        api_views.DeleteScreenshot.as_view()
    )
]