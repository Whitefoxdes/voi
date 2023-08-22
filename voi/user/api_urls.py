from . import api_views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )

app_name = "user_api"

urlpatterns = [
    path(
        'register',
        api_views.Register.as_view(),
        name='register'
    ),
    path(
        'login',
        TokenObtainPairView.as_view(),
        name='login'
    ),
    path(
        'token-refresh',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'profile',
        api_views.UserProfile.as_view(),
        name="user_profile"
    ),
    path(
        'edit-profile',
        api_views.EditProfile.as_view(),
        name='edit_profile'
    ),
    path(
        'edit-email',
        api_views.EditEmail.as_view(),
        name='edit_email'
    ),
    path(
        'change-password',
        api_views.ChangePassword.as_view(),
        name='change_password'
    ),
    path(
        'activate-user/<uuid:user_activation_uuid>',
        api_views.ActivateUser.as_view(),
        name='activate_user'
    ),
    path(
        'send-reset-password-letter',
        api_views.SendResetPasswordLetter.as_view(),
        name='send_reset_password_letter'
    ),
    path(
        'reset-password/<str:reset_password_uuid>',
        api_views.ResetPassword.as_view(),
        name='reset_password'
    ),
    path(
        'user-avatar-upload',
        api_views.UserAvatarUpload.as_view(),
        name='user_avatar_upload'
    )
]