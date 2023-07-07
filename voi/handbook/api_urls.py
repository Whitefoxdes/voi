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
        name='handbook_type_list'
    ),
    path(
        "upload-screenshot-for-handbook/<int:handbook_id>",
        api_views.ScreenshotUpload.as_view(),
        name='screenshot_upload'
    ),
    re_path(
        r"handbook-list/$",
        api_views.AllHandbookList.as_view(),
        name='handbook_list'
    ),
    path(
        "<int:handbook_id>",
        api_views.HandbookInfo.as_view(),
        name='handbook_info'
    ),
    path(
        "edit/<int:handbook_id>",
        api_views.EditHandbook.as_view(),
        name='edit_handbook'
    ),
    path(
        "delete/<int:handbook_id>",
        api_views.DeleteHandbook.as_view(),
        name='delete_handbook'
    ),
    path(
        "delete-screenshot",
        api_views.DeleteScreenshot.as_view(),
        name='delete_screenshot'
    )
]