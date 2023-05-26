from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView 

app_name = "user"

urlpatterns = [
    path('register', views.RegisterRender.as_view(), name='register'),
    path('login', views.LoginRender.as_view(), name='login'),
    path('profile', views.UserProfileRender.as_view(), name='profile')
]