from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password'
        ]
    def validate_registrate_field(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            raise serializers.ValidationError({"error": "Request fields empty"})
        
        return data
    
    def validate_login_field(self, data):
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            raise serializers.ValidationError({"error": "Request fields empty"})
        
        return data