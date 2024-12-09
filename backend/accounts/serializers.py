from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        email = validated_data.pop('email')
        user = User.objects.create_user(username=email, email=email, **validated_data)
        user.profile.phone_number = phone_number
        user.profile.save()
        return user