from uuid import uuid4
from .models import (
    User, 
    Profile,
    ImageProfile)
from django.shortcuts import render
from .serializer import (
    UserSerializer,
    ProfileSerializer,
    ImageProfileSerializer
)
from voi.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
import datetime
# Create your views here.

class Register(APIView):    
    def post(self, request):
        
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid()
        
        data_user =  user_serializer.validated_data
        
        if User.objects.filter(email=data_user["email"]).exists():
            return Response({"error_email_exist":"Email exist"}, status=400)

        profile_serializer = ProfileSerializer(data=request.data)
        profile_serializer.is_valid()
        data_profile = profile_serializer.validated_data

        new_profile = Profile(
            username = data_profile.get("username"),
            date_of_birth = data_profile.get("date_of_birth")
        )
        
        new_profile.save()
        new_profile.user_avatar
        new_user = User(
            email = data_user.get("email"),
            password = make_password(data_user.get("password")),
            user_activation_uuid = uuid4(),
            profile = new_profile,
        )

        # new_user.set_password(test.get(password))
        # new_user.profile = new_p
        # new_user.profile.username = "jesi"
        # new_user.profile.date_of_birth = "2000-01-01"
        # new_profile.save()
        # file.save()
        # new_user.save()
        # new_user.refresh_from_db()

        # import pdb; pdb.set_trace()
        # new_profile = Profile.objects.create(username = data_profile.get("username"), date_of_birth = data_profile.get("date_of_birth"))
        # file = Profile.objects.create()
        # new_user = Profile.objects.create()

        # new_profile.username = data_profile.get("username")
        # new_profile.date_of_birth = data_profile.get("date_of_birth")
        # file.user_profile = new_profile
        # new_profile.user_avatar = file
        # new_user.email = data_user.get("email"),
        # new_user.password = make_password(data_user.get("password")),
        # new_user.user_activation_uuid = uuid4(),
        # new_user.profile = new_profile,
        
        # new_profile.save()
        new_user.save()

        send_mail(
                subject = f'Hello {new_profile.username}',
                message = f"Account activation link http://127.0.0.1:8000/user/activate-user/{new_user.user_activation_uuid}",
                from_email = EMAIL_HOST_USER,
                recipient_list = [f'{new_user.email}'],
                fail_silently = False
        )

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
    def put(self, request):
        
        user_id = request.user.id

        serializer = ProfileSerializer(data=request.data)
        serializer.validate({"username": request.data["username"]})
        serializer.is_valid()

        # error = serializer.errors.get("username")
        # if error:
        #     return Response({"error": "Username field empty"}, status=400)

        data = serializer.validated_data

        import pdb; pdb.set_trace()

        user = User.objects.filter(pk=user_id).first()

        user.username = data.get('username')
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)

class EditEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        
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

        if not check_password(data.get("password"), user.password):
            return Response({"error_confirm_identity_password": "Wrong password"}, status=400)

        user.email = data.get('email')
        user.save()
        user.refresh_from_db()

        return Response({"status": "Update"}, status=200)
    
class EditDateOfBirth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):
        
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
    def put(self, request):
        
        user_id = request.user.id

        serializer = UserSerializer(data=request.data)
        serializer.check_old_password(data={"old_password": request.data.get("old_password"), "user_id": user_id})
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
    
class ActivateUser(APIView):
    def put(self, request, user_activation_number):
        
        user = User.objects.filter(user_activation_uuid = user_activation_number, is_active = False).first()
        if not user: 
            return Response({"error_user": "Your account already activate or URL incapacitated"}, status=400)
        
        user.is_active = True
        user.save()
        user.refresh_from_db()
        return Response({"status": "Activate"}, status=200)
    
class SendResetPasswordLetter(APIView):
    def post(self, request):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("email")
        if error:
            return Response({"error": "Request field empty"}, status=400)

        data = serializer.data

        user = User.objects.filter(email=data.get("email")).first()

        if not user:
            return Response({"error_not_found_email": "Not found user with this email"}, status=404)
        
        user.reset_password_number = uuid4()
        user.save()
        user.refresh_from_db()

        send_mail(
            subject = f'Hello {user.username}',
            message = f"Reset password link http://127.0.0.1:8000/user/reset-password/{user.reset_password_number}",
            from_email = EMAIL_HOST_USER,
            recipient_list = [f'{user.email}'],
            fail_silently = False
        )
        return Response({"status": "Send"}, status=200)
    
class ResetPassword(APIView):
    def put(self,request, reset_password_number):
        
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()

        error = serializer.errors.get("password")
        if error:
            return Response({"error": "Password field empty"}, status=400)
        
        data = serializer.data

        user = User.objects.filter(reset_password_number = reset_password_number).first()

        if not user:
            return Response({"error_url":"URL incapacitated"}, status = 404)
        
        user.reset_password_number = None
        user.set_password(data.get('password'))
        user.save()
        user.refresh_from_db()

        return Response({"status":"Reset"}, status=200)
    
class test(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):

        user_id = request.user.id

        serializer = ImageProfileSerializer(data=request.FILES)

        serializer.is_valid()
        data = serializer.validated_data

        user = User.objects.filter(pk=user_id).first()
        file = ImageProfile()

        file.user_id = user

        file.file_url = data["file_url"]
        file.save()
        user.user_avatar = file
        user.save()

        return Response({'status': "Upload"}, status=200)