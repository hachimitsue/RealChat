# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Message

from cryptography.fernet import Fernet
import base64
import os
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, phone_number=phone_number)
        return user
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        key = os.getenv('ENCRYPTION_KEY').encode()  # Load key from environment variable
        cipher_suite = Fernet(key)
        try:
            encrypted_content = representation['content']
            logger.debug(f"Encrypted message content: {encrypted_content}")
            decrypted_content = cipher_suite.decrypt(base64.urlsafe_b64decode(self.ensure_padding(encrypted_content)))
            representation['content'] = decrypted_content.decode('utf-8')
            logger.debug(f"Decrypted message content: {representation['content']}")
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            representation['content'] = f"Decryption error: {e}"
        return representation

    def ensure_padding(self, data):
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return data
    def ensure_padding(self, data):
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return data