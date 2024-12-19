from django.urls import path
from .views import RegisterView, LoginView, MessageListView, SendMessageView, ReceiveMessageView, protected_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', protected_view, name='protected'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('receive-message/', ReceiveMessageView.as_view(), name='receive-message'),
]