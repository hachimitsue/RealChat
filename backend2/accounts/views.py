# accounts/views.py
import os
import base64

from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from cryptography.fernet import Fernet

from .serializers import UserSerializer, MessageSerializer
from .models import Profile, Message

import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view"}, status=200)

class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = os.getenv('ENCRYPTION_KEY').encode()  # Load key from environment variable
        self.cipher_suite = Fernet(self.key)

    def post(self, request):
        try:
            logger.debug(f"Original request data: {request.data}")
            encrypted_content = self.cipher_suite.encrypt(request.data['content'].encode())
            encoded_content = base64.urlsafe_b64encode(encrypted_content).decode('utf-8')
            request.data['content'] = encoded_content
            request.data['sender'] = request.user.id  # Set the sender to the authenticated user
            logger.debug(f"Modified request data: {request.data}")
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in post method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            logger.debug(f"Serialized messages: {serializer.data}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in get method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message')
        key = os.getenv('ENCRYPTION_KEY').encode()
        cipher = Fernet(key)
        encrypted_message = cipher.encrypt(message.encode())
        
        # Send encrypted message to backend
        response = requests.post('http://127.0.0.1:8000/accounts/receive-message/', data={'message': encrypted_message})
        return Response(response.json())

class ReceiveMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        encrypted_message = request.data.get('message')
        key = os.getenv('ENCRYPTION_KEY').encode()
        cipher = Fernet(key)
        decrypted_message = cipher.decrypt(encrypted_message.encode()).decode()
        return Response({'message': decrypted_message})