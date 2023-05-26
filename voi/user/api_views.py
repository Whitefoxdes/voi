from .models import User
from django.shortcuts import render
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication 
# Create your views here.

class Register(APIView):    
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
        
class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):

        user_id = request.user.id

        user = User.objects.filter(pk=user_id).first()
        
        serializer = UserSerializer(user)
            
        return Response({"data": serializer.data}, status=200)
    
class EditUsername(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user_id = request.user.id

        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("username")
        if error:
            return Response({"error": "Username field empty"}, status=400)

        data = serializer.data
        user = User.objects.filter(pk=user_id).first()

        user.username = data.get('username')
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)

class EditEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user_id = request.user.id

        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("email")
        if error:
            return Response({"error": "Email field empty"}, status=400)
        
        data = serializer.data

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error_email_exist":"Email exist"}, status=400)


        user = User.objects.filter(pk=user_id).first()

        user.email = data.get('email')
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)
    
class EditDateOfBirth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user_id = request.user.id

        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("date_of_birth")
        if error:
            return Response({"error": "Date of birth field empty"}, status=400)
        
        data = serializer.data

        user = User.objects.filter(pk=user_id).first()

        user.date_of_birth = data.get('date_of_birth')
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)

class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        user_id = request.user.id

        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("password")
        if error:
            return Response({"error": "Password field empty"}, status=400)
        
        data = serializer.data

        user = User.objects.filter(pk=user_id).first()

        user.set_password(data.get('password'))
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)
