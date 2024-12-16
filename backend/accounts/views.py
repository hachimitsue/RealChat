import base64

from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, generics
from rest_framework.response import Response            
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import UserSerializer, MessageSerializer
from .models import Profile, Message

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):    
    """
    Handles user registration.
    """
    def post(self, request):
        # Deserialize the request data and validate it
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and create a token
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)
        # Return validation errors if the data is invalid
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    Handles user login.
    """
    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if both username and password are provided
        if not username or not password:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in and create a token
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)
        else:
            # Return an invalid credentials response
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    """
    A protected view that requires authentication.
    """
    return Response({"message": "This is a protected view"}, status=200)


class MessageListView(generics.ListCreateAPIView):
    """
    Handles listing and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the message with the sender set to the current user
        serializer.save(sender=self.request.user)