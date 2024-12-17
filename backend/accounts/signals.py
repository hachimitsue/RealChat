from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Signal to create a user profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile instance whenever a new User instance is created.
    """
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)

# Signal to save the user profile when the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Ensures the Profile instance is saved whenever the User instance is saved.
    """
    # Ensure the profile exists before saving
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()