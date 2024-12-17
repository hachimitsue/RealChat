from django.contrib import admin
from .models import UserInfo

# Register the UserInfo model with the admin site
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    """
    Admin view for the UserInfo model.
    """
    list_display = ('user', 'phone_number')