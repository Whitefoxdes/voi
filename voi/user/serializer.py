from .models import User
from rest_framework import serializers
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "date_of_birth"
        ]

    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    date_of_birth = serializers.DateTimeField()