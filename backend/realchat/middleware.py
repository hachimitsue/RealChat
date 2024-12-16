import base64
from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin

class EncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def process_request(self, request):
        if request.method == 'POST' and request.path == '/accounts/messages/':
            try:
                encrypted_body = self.cipher_suite.encrypt(request.body)
                encoded_body = base64.urlsafe_b64encode(encrypted_body).decode('utf-8')
                request._body = encoded_body.encode('utf-8')
            except Exception as e:
                print(f"Encryption error: {e}")

    def process_response(self, request, response):
        if response.status_code == 200 and request.path == '/accounts/messages/':
            try:
                decoded_content = base64.urlsafe_b64decode(response.content)
                decrypted_content = self.cipher_suite.decrypt(decoded_content)
                response.content = decrypted_content
            except Exception as e:
                print(f"Decryption error: {e}")
        return response