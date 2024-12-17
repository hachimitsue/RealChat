from django.contrib import admin
from .models import Profile, Message

# Register the Profile model with the admin site
admin.site.register(Profile)

# Register the Message model with the admin site
admin.site.register(Message)