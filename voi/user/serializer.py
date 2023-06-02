from .models import (
    User,
    ImageProfile,
    Profile)
from rest_framework import serializers
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    email = serializers.CharField()
    password = serializers.CharField()
        
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = [
            "username",
            "date_of_birth",
            "user_avatar"
        ]

    username = serializers.CharField()
    date_of_birth = serializers.DateTimeField()
    user_avatar = serializers.CharField(source="user_avatar.file_url", required=False)

    def check_old_password(self, data):
        old_password = data.get("old_password")
        user_id = data.get("user_id")

        user = User.objects.filter(pk=user_id).first()

        if not check_password(old_password, user.password):
            raise serializers.ValidationError({"error_old_password": "Wrong old password"})
        
    

class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = [
            "file_url"
        ]
    file_url = serializers.FileField(write_only=True)