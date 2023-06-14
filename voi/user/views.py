from django.shortcuts import render
from rest_framework.views import APIView

class RegisterRender(APIView):
    def get(self, request):
        return render(request,"register.html")
    
class LoginRender(APIView):
    def get(self, request):
        return render(request, "login.html")


class UserProfileRender(APIView):
    def get(self, request):
        return render(request, 'profile.html')
    
class ActivateUserRender(APIView):
    def get(self, request, user_activate_number):
        return render(request, "activate_user.html", context={"user_activate_number": user_activate_number})
    
class SendResetPasswordLetterRender(APIView):
    def get(self, request):
        return render(request, "send_reset_password_letter.html")

class ResetPasswordRender(APIView):
    def get(self, request, reset_password_number):
        return render(request, "reset_password.html", context={"reset_password_number": reset_password_number})