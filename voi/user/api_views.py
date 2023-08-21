from .models import (
    User, 
    Profile,
    ImageProfile
    )
from uuid import uuid4
from .serializer import (
    UserSerializer,
    ProfileSerializer,
    ImageProfileSerializer
    )
from voi.settings import (
    EMAIL_HOST_USER,
    ALLOWED_FILE_EXT,
    FILE_UPLOAD_MAX_MEMORY_SIZE,
    )
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.contrib.auth.hashers import (
    make_password,
    check_password
    )
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class Register(APIView):
    def post(
            self,
            request):

        user_serializer = UserSerializer(data=request.data)

        user_serializer.is_valid()
        if user_serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data_user =  user_serializer.validated_data

        if User.objects.filter(email=data_user["email"]).exists():
            return Response(
                {"error_email_exist":"Email exist"},
                status=400)

        profile_serializer = ProfileSerializer(data=request.data)

        profile_serializer.is_valid()
        if profile_serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data_profile = profile_serializer.validated_data

        new_profile = Profile(
            username=data_profile.get("username"),
            date_of_birth=data_profile.get("date_of_birth")
        )

        new_profile.save()

        new_user = User(
            email=data_user.get("email"),
            password=make_password(data_user.get("password")),
            user_activation_uuid=uuid4(),
            profile=new_profile,
        )

        new_user.save()

        new_user_activation_uuid = new_user.user_activation_uuid
        activate_user_url = f"http://127.0.0.1:8000/user/activate-user/"
        msg_url = f"{activate_user_url}{new_user_activation_uuid}"

        send_mail(
            subject=f"Hello {new_profile.username}",
            message=f"Account activation link {msg_url}",
            from_email= EMAIL_HOST_USER,
            recipient_list=[f'{new_user.email}'],
            fail_silently=False)

        return Response(
            {"status":"Register"},
            status=200)
        
class UserProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
            self,
            request):

        user_id = request.user.id

        user = User.objects.filter(pk=user_id).first()
        serializer_user = UserSerializer(user)
        serializer_profile = ProfileSerializer(user.profile) 
        data_user = serializer_user.data
        data_profile = serializer_profile.data

        return Response(
            {
                "data_user": data_user,
                "data_profile": data_profile
            },
            status=200)

class EditEmail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request):

        user_id = request.user.id

        serializer = UserSerializer(data=request.data)

        serializer.is_valid()
        if serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data = serializer.validated_data

        if User.objects.filter(email=data["email"]).exists():
            return Response(
                {"error_email_exist":"Email exist"},
                status=400)

        user = User.objects.filter(pk=user_id).first()

        if not check_password(data.get("password"), user.password):
            return Response(
                {"error_confirm_identity_password": "Wrong password"},
                status=400)

        user.email = data.get('email')
        user.save()
        user.refresh_from_db()

        return Response(
            {"status": "Update"},
            status=200)

class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request):

        user_id = request.user.id

        serializer = UserSerializer(data=request.data)

        serializer.check_old_password(
            data={
                "old_password": request.data.get("old_password"),
                "user_id": user_id
            }
        )

        serializer.is_valid()
        if serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data = serializer.validated_data
        user = User.objects.filter(pk=user_id).first()

        user.set_password(data.get('password'))
        user.save()
        user.refresh_from_db()

        msg_url = "http://127.0.0.1:8000/user/send-reset-password-letter"
        email_msg = f"Your password has been changed. If you weren't change password {msg_url}"
        send_mail(
            subject=f'Hello {user.profile.username}',
            message=email_msg,
            from_email=EMAIL_HOST_USER,
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )

        return Response(
            {"status": "Update"},
            status=200)

class EditProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request):

        user_id = request.user.id

        serializer = ProfileSerializer(data=request.data)
        
        serializer.is_valid()
        if serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data = serializer.validated_data

        profile = Profile.objects.filter(user__id=user_id).first()
        profile.username = data.get('username')
        profile.date_of_birth = data.get('date_of_birth')

        profile.save()
        profile.refresh_from_db()

        return Response(
            {"status": "Update"},
            status=200)

class UserAvatarUpload(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(
            self,
            request):

        user_id = request.user.id

        serializer = ImageProfileSerializer(data=request.FILES)
        
        serializer.is_valid()
        if serializer.errors:
            return Response(
                {"error": "Request field empty"},
                status=400)

        data = serializer.validated_data

        if data.get("file_url").size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            return Response(
                {"error_file_size": "File size is too large"},
                status=400)

        file_ext = data.get("file_url").name.split(".")[1]

        if file_ext not in ALLOWED_FILE_EXT:
            return Response(
                {"error_file_ext": "Invalid file type"},
                status=400)

        profile = Profile.objects.filter(user__id=user_id).first()
        
        new_file = ImageProfile()

        new_file.user_profile = profile
        new_file.file_url = data.get("file_url")
        new_file.save()

        profile.user_avatar = new_file
        profile.save()

        return Response(
            {'status': "Upload"},
            status=200)

class ActivateUser(APIView):
    def put(
            self,
            request,
            user_activation_uuid):

        user = User.objects.filter(
            user_activation_uuid=user_activation_uuid,
            is_active = False).first()
        if not user:
            error_msg = "Your account already activate or URL incapacitated"
            return Response(
                {"error_user": error_msg},
                status=400)

        user.is_active = True
        user.save()
        user.refresh_from_db()
        return Response(
            {"status": "Activate"},
            status=200)
    
class SendResetPasswordLetter(APIView):
    def post(self, request):

        serializer = UserSerializer(data=request.data)

        serializer.send_reset_password_letter_serializer(
            data={
                "email": request.data.get("email")
            }
        )

        serializer.is_valid()

        data = serializer.data

        user = User.objects.filter(email=data.get("email")).first()

        if not user:
            return Response(
                {"error_not_found_email": "Not found user with this email"},
                status=404)

        user.reset_password_uuid = uuid4()
        user.save()
        user.refresh_from_db()

        user_reset_password_uuid = user.reset_password_uuid
        reset_password_url = "http://127.0.0.1:8000/user/reset-password/"
        msg_url = f"{reset_password_url}{user_reset_password_uuid}"

        send_mail(
            subject=f'Hello {user.profile.username}',
            message=f"Reset password link {msg_url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )

        return Response(
            {"status": "Send"},
            status=200)

class ResetPassword(APIView):
    def put(
            self,
            request,
            reset_password_uuid):

        serializer = UserSerializer(data=request.data)
        
        serializer.reset_password_serializer(
            data={
                "password": request.data.get("password")
            }
        )
        serializer.is_valid()

        data = serializer.data

        user = User.objects.filter(reset_password_uuid=reset_password_uuid).first()

        if not user:
            return Response(
                {"error_url":"URL incapacitated"},
                status = 404)

        user.reset_password_uuid = None
        user.set_password(data.get('password'))
        user.save()
        user.refresh_from_db()

        return Response({"status":"Reset"}, status=200)