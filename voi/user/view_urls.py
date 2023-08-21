from . import views
from django.urls import path

app_name = "user_view"

urlpatterns = [
    path(
        'register',
        views.RegisterRender.as_view(),
        name='register'
    ),
    path(
        'login',
        views.LoginRender.as_view(),
        name='login'
    ),
    path(
        'profile',
        views.UserProfileRender.as_view(),
        name='profile'
    ),
    path(
        'activate-user/<uuid:user_activate_uuid>',
        views.ActivateUserRender.as_view(),
        name='activate_user'
    ),
    path(
        'send-reset-password-letter',
        views.SendResetPasswordLetterRender.as_view(),
        name='send_reset_password_letter'
    ),
    path(
        'reset-password/<str:reset_password_uuid>',
        views.ResetPasswordRender.as_view(),
        name='reset_password'
    ),
]