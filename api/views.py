import jwt
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from django.contrib.auth.models import User
from django.shortcuts import render
from clients.models import Clients

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Проверка, есть ли пользователь в request
        if hasattr(request, 'user'):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({'auth': None})

        # Если пользователя нет, читаем JWT токен из заголовка Authorization
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

            return view_func(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return wrapper


@jwt_required
def add_client(request):
    return JsonResponse({'success': True})

@jwt_required
def get_client(request, id):
    return None


def get_all_clients(request):
    return None


def edit_client(request, id):
    return None


def delete_client(request, id):
    return None



def add_orders(request):
    return None


def get_order(request, id):
    return None


def add_order(request, id):
    return None


def delete_order(request):
    return None


def get_all_orders(request):
    return None


def delete_orders(request):
    return None