import jwt
from django.shortcuts import render
from .settings import SECRET_KEY
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.hashers import check_password, make_password

@api_view(['GET', 'POST'])
def index(request):
    if request.method == "GET":
        return render(request, "index.html")