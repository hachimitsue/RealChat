from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        # Check if a Profile already exists for the user
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, phone_number=phone_number)
        return user