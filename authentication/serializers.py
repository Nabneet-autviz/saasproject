from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)  
    class Meta:
        model =CustomUser
        fields="__all__"
        fields = ('id','username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)

        return user
    
