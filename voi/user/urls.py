from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/registrate', views.registrate),
    path('api/v1/login', views.login)
]