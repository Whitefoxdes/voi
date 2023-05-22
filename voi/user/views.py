from .models import User
from django.shortcuts import render
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
# Create your views here.

class Register(APIView):
    def get(self, request):
        return render(request,"register.html")
    
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error_field_empty": "Request field empty"}, status=400)
        data = serializer.data

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error_email_exist":"Email exist"}, status=400)

        new_user = User(
            username=data.get("username"),
            email = data.get("email"),
            password = make_password(data.get("password")),
            date_of_birth = data.get("date_of_birth")
        )

        new_user.save()
        new_user.refresh_from_db()
        
        return Response({"status":"Register"}, status=200)
    

class Login(APIView):
    def get(self, request):
        return render(request, "login.html")