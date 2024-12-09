from django.http import JsonResponse
from django.views import View
import vonage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

@method_decorator(csrf_exempt, name='dispatch')
class SendSMSView(View):
    def post(self, request):
        data = json.loads(request.body)
        phone_number = data.get('phone_number')

        if not phone_number:
            return JsonResponse({"message": "Phone number is required"}, status=400)

        client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
        sms = vonage.Sms(client)

        responseData = sms.send_message({
            "from": settings.VONAGE_BRAND_NAME,
            "to": phone_number,
            "text": "You have successfully registered to RealChat",
        })

        if responseData["messages"][0]["status"] == "0":
            return JsonResponse({"message": "Message sent successfully"})
        else:
            return JsonResponse({"message": "Message failed with error: " + responseData["messages"][0]["error-text"]}, status=500)