from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

app_name = "user"

urlpatterns = [
    path('register', views.Register.as_view(http_method_names=["get"]), name='register'),
    path('login', views.Login.as_view(http_method_names=["get"]), name='login'),
    path('test', views.Test.as_view(), name='test'),
]