import base64
from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin
import logging
import os

logger = logging.getLogger(__name__)

class EncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.key = os.getenv('ENCRYPTION_KEY').encode()  # Load key from environment variable
        self.cipher_suite = Fernet(self.key)

    def process_request(self, request):
        if request.method == 'POST' and request.path == '/accounts/messages/':
            try:
                encrypted_body = request.body
                decrypted_body = self.cipher_suite.decrypt(base64.urlsafe_b64decode(self.ensure_padding(encrypted_body)))
                request._body = decrypted_body
            except Exception as e:
                logger.error(f"Decryption error: {e}")
                logger.error(f"Request body: {request.body}")

    def process_response(self, request, response):
        if request.method == 'POST' and request.path == '/accounts/messages/':
            try:
                encrypted_content = response.content
                decrypted_content = self.cipher_suite.decrypt(base64.urlsafe_b64decode(self.ensure_padding(encrypted_content)))
                response.content = decrypted_content
            except Exception as e:
                logger.error(f"Decryption error: {e}")
        return response

    def ensure_padding(self, data):
        missing_padding = len(data) % 4
        if missing_padding:
            data += b'=' * (4 - missing_padding)
        return data