from .models import User
from django.shortcuts import render
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterRender(APIView):
    def get(self, request):
        return render(request,"register.html")
    
class LoginRender(APIView):
    def get(self, request):
        return render(request, "login.html")


class UserProfileRender(APIView):
    def get(self, request):
        return render(request, 'profile.html')