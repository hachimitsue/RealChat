import os
import base64
import requests
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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

# Set up logging for the views module of the accounts app (logs to console)
logger = logging.getLogger(__name__)

# User Registration View
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """
    Handles user registration.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        # Validate the serializer and save the user if valid with a token response
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Handles user login.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the username and password are provided
        if not username or not password:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user and return a token if successful
        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated and return a token
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Protected View Example
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    Example of a protected view that requires authentication.
    """
    return Response({"message": "This is a protected view"}, status=200)

# Message List View (Handles sending and retrieving messages)
class MessageListView(APIView):
    """
    Handles sending and retrieving messages.
    """
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = os.getenv('ENCRYPTION_KEY').encode() 
        self.cipher_suite = Fernet(self.key)

    def post(self, request):
        """
        Encrypts and sends a message.
        """
        try:
            logger.debug(f"Original request data: {request.data}")
            encrypted_content = self.cipher_suite.encrypt(request.data['content'].encode())
            encoded_content = base64.urlsafe_b64encode(encrypted_content).decode('utf-8')
            request.data['content'] = encoded_content
            request.data['sender'] = request.user.id  
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
        """
        Retrieves messages for the authenticated user.
        """
        try:
            user = request.user
            messages = Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
            serializer = MessageSerializer(messages, many=True)
            logger.debug(f"Serialized messages: {serializer.data}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in get method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Send Message View (Handles sending messages to another backend)
class SendMessageView(APIView):
    """
    Handles sending messages to another backend.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Encrypts and sends a message to another backend.
        """
        message = request.data.get('message')
        receiver_username = request.data.get('receiver')
        key = os.getenv('ENCRYPTION_KEY').encode()
        cipher = Fernet(key)
        encrypted_message = cipher.encrypt(message.encode())

        # Get the token for the authenticated user
        token = Token.objects.get(user=request.user).key
        logger.debug(f"Sending token: {token}")

        # Check if the receiver exists
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Send encrypted message to backend
        response = requests.post(
            'http://127.0.0.1:8000/accounts/receive-message/',
            data={'message': base64.urlsafe_b64encode(encrypted_message).decode('utf-8'), 'sender': request.user.username, 'receiver': receiver_username},
            headers={'Authorization': f'Token {token}'}
        )

        # Log the response content for debugging
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response content: {response.text}")

        # Check if the response is valid JSON
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Invalid JSON response: {response.text}")
            return Response({"error": "Invalid response from backend"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.debug(f"Response: {response_data}")

        return Response(response_data)

# Receive Message View (Handles receiving messages from another backend)
class ReceiveMessageView(APIView):
    """
    Handles receiving messages from another backend.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Decrypts and saves a received message.
        """
        encrypted_message = request.data.get('message')
        sender_username = request.data.get('sender')
        receiver_username = request.data.get('receiver')
        key = os.getenv('ENCRYPTION_KEY').encode()
        cipher = Fernet(key)
        decrypted_message = cipher.decrypt(base64.urlsafe_b64decode(encrypted_message)).decode()

        # Check if the sender exists
        try:
            sender = User.objects.get(username=sender_username)
        except User.DoesNotExist:
            return Response({"error": "Sender does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the receiver exists
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the message to the database
        Message.objects.create(sender=sender, receiver=receiver, content=encrypted_message)

        return Response({'message': decrypted_message}, status=status.HTTP_200_OK)