from functools import wraps

import jwt
from django.http import JsonResponse
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.auth.models import User


from OrderAndCustomerAccountingSystem import settings


def jwt_or_csrf_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        csrf_middleware = CsrfViewMiddleware(lambda r: r)
        csrf_result = csrf_middleware.process_view(request, None, (), {})


        if csrf_result is None:
            if hasattr(request, 'user'):
                if request.user.is_authenticated:
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'success': False, 'error':'not auth'})

        # Проверяем JWT токен
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization header is missing or invalid'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            if not user_id:
                return JsonResponse({'error': 'Invalid token payload'}, status=401)

            user = User.objects.get(id=user_id)
            request.user = user
            print("JWT token is valid. User authenticated by JWT.")
            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return wrapper
