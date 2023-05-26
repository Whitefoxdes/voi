from . import api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

app_name = "user_api"

urlpatterns = [
    path('register', api_views.Register.as_view(), name='register'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', api_views.UserProfile.as_view(), name="user_profile"),
    path('edit-username', api_views.EditUsername.as_view(), name='edit_username'),
    path('edit-email', api_views.EditEmail.as_view(), name='edit_email'),
    path('edit-date-of-birth', api_views.EditDateOfBirth.as_view(), name='edit_date_of_birth'),
    path('change-password', api_views.ChangePassword.as_view(), name='change_password'),
]