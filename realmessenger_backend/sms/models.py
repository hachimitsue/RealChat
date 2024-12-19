from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    """
    Model to store additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"