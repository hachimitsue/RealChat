import os
from os.path import join, dirname
from dotenv import load_dotenv
from vonage import Auth, Vonage
from vonage_sms import SmsMessage, SmsResponse

# Load environment variables from .env file
dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

VONAGE_API_KEY = os.getenv('VONAGE_API_KEY')
VONAGE_API_SECRET = os.getenv('VONAGE_API_SECRET')
VONAGE_BRAND_NAME = os.getenv("VONAGE_BRAND_NAME")

def send_sms(to, message):
    client = Vonage(Auth(api_key=VONAGE_API_KEY, api_secret=VONAGE_API_SECRET))

    sms_message = SmsMessage(
        to=to,
        from_=VONAGE_BRAND_NAME,
        text=message,
    )

    response: SmsResponse = client.sms.send(sms_message)
    if response.messages[0].status != '0':
        raise Exception(f"Message failed with error: {response.messages[0].error_text}")