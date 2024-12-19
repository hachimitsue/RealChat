import os
import base64
import logging

from cryptography.fernet import Fernet
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Message

# Set up logging
logger = logging.getLogger(__name__)

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates a new user and a profile for the user.
        """
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(user=user, phone_number=phone_number)
        return user
    
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

# Serializer for Message model
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'sender_username', 'receiver_username', 'content', 'timestamp']

    def to_representation(self, instance):
        """
        Decrypts the message content before returning the representation.
        """
        representation = super().to_representation(instance)
        key = os.getenv('ENCRYPTION_KEY').encode()  
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
        """
        Ensures the base64 encoded data has the correct padding.
        """
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return data