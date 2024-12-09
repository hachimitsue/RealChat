from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]