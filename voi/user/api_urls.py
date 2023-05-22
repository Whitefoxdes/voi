from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

app_name = "user_api"

urlpatterns = [
    path('register', views.Register.as_view(http_method_names=["post"]), name='register'),
    path('login', TokenObtainPairView.as_view(http_method_names=["post"]), name='login'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]