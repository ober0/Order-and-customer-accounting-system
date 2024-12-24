import logging

logger = logging.getLogger(__name__)

class LogRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логирование информации о запросе
        logger.info(f"Request: {request.method} {request.get_full_path()}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request.body.decode('utf-8', errors='replace')}")

        response = self.get_response(request)

        # Логирование информации о ответе (необязательно)
        logger.info(f"Response: {response.status_code}")
        return response
