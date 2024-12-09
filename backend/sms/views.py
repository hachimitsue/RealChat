from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import send_sms
from .models import UserInfo
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if not email or not password or not phone_number:
            return JsonResponse({'error': 'Missing fields'}, status=400)

        if User.objects.filter(username=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()

        # Save user info
        user_info = UserInfo(user=user, phone_number=phone_number)
        user_info.save()

        try:
            # Send SMS
            send_sms(phone_number, 'You have successfully signed up!')
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return JsonResponse({'error': 'User created but failed to send SMS'}, status=500)

        return JsonResponse({'message': 'User created and SMS sent!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)