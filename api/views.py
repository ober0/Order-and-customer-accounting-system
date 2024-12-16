import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from django.contrib.auth.models import User
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import csrf_exempt


def jwt_or_csrf_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print("Checking CSRF token...")

        # Инициализируем CSRF Middleware с заглушкой get_response
        csrf_middleware = CsrfViewMiddleware(lambda r: r)
        csrf_result = csrf_middleware.process_view(request, None, (), {})

        # Если process_view ничего не вернул, значит CSRF проверка пройдена
        if csrf_result is None:
            # Проверим аутентификацию пользователя по сессии
            if hasattr(request, 'user'):
                if request.user.is_authenticated:
                    print("CSRF token is valid and user is authenticated by session.")
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'auth': None})

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

@csrf_exempt
@jwt_or_csrf_required
def add_client(request):
    return JsonResponse({'auth': request.user.username})

@jwt_or_csrf_required
def get_client(request, id):
    return None

@jwt_or_csrf_required
def get_all_clients(request):
    return None

@jwt_or_csrf_required
def edit_client(request, id):
    return None

@jwt_or_csrf_required
def delete_client(request, id):
    return None


@jwt_or_csrf_required
def add_orders(request):
    return None

@jwt_or_csrf_required
def get_order(request, id):
    return None

@jwt_or_csrf_required
def add_order(request, id):
    return None

@jwt_or_csrf_required
def delete_order(request):
    return None

@jwt_or_csrf_required
def get_all_orders(request):
    return None

@jwt_or_csrf_required
def delete_orders(request):
    return None