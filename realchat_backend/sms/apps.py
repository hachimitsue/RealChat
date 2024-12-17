from django.apps import AppConfig

class SmsServiceConfig(AppConfig):
    """
    Configuration for the SMS service app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms'