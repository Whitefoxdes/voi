import jwt
from .models import User
from django.shortcuts import render
from voi.settings import SECRET_KEY
from django.http import JsonResponse
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.


@api_view(['GET', 'POST'])
def registrate(request):
    
    if request.method == "POST":
        user_data = request.data
        
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        
        UserSerializer().validate_registrate_field(data={
            "username" : username,
            "email" : email,
            "password" : password
        })

        if User.objects.filter(email=email).exists():
            return Response({"error":"Email exist"}, status=400)

        new_user = User(
            username=username,
            email = email,
            password = make_password(password)
        )

        new_user.save()
        new_user.refresh_from_db()
        
        return Response({"status: Registrate"}, status=200)

@api_view(['GET', 'POST'])
def login(request):
    if request.method == "POST":
        
        user_data = request.data
        email = user_data.get("email")
        password = user_data.get("password")

        UserSerializer().validate_login_field(data={
            "email": email,
            "password": password
        })

        user = User.objects.filter(email = email).first()

        if not user:
            return Response({"error":  "Wrong email or password"}, status=400)

        if not check_password(password, user.password):
            return Response({"error":  "Wrong email or password"}, status=400)
        
        return Response({"token":str(AccessToken.for_user(user))}, status=200)