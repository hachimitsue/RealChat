from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Profile model to store additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"

class Message(models.Model):
    """
    Message model to store messages between users.
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp}"