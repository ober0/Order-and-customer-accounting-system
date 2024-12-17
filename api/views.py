import json

import jwt
from django.db.models import Subquery
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.conf import settings
from functools import wraps
from django.contrib.auth.models import User
from django.middleware.csrf import CsrfViewMiddleware
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from clients.models import Clients
from orders.models import Orders


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


@jwt_or_csrf_required
def add_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        mobile_phone = request.POST.get('mobile_phone')
        email = request.POST.get('email')


        if not first_name or not last_name or not email:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            client = Clients.objects.create(
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                mobile_phone=mobile_phone,
                email=email
            )
            client.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False,'error': str(e)})

@jwt_or_csrf_required
def get_client(request, id):
    if request.method == 'POST':
        client = get_object_or_404(Clients, id=id)

        client_data = {
            'id': client.id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'middle_name': client.middle_name,
            'mobile_phone': client.mobile_phone,
            'email': client.email,
        }
        return JsonResponse({'client': client_data})



@csrf_exempt
@jwt_or_csrf_required
def get_all_clients(request):
    if request.method == 'POST':
        try:
            start_id = int(request.POST.get('start_id', None))
            print(start_id)
            if start_id is None or not isinstance(start_id, int):
                return JsonResponse({'error': 'start_id parameter is required and must be an integer'}, status=400)

            clients = Clients.objects.filter(id__gte=start_id).order_by('id')[:20]

            if not clients.exists():
                return JsonResponse({'clients': [], 'message': 'No clients found'}, status=200)


            clients_data = [
                {
                    'id': client.id,
                    'first_name': client.first_name,
                    'last_name': client.last_name,
                    'middle_name': client.middle_name,
                    'mobile_phone': client.mobile_phone,
                    'email': client.email,
                }
                for client in clients
            ]

            return JsonResponse({'clients': clients_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
def edit_client(request, id):
    if request.method == 'POST':
        try:
            body = request.POST
            client = get_object_or_404(Clients, id=int(id))

            first_name = body.get('first_name', client.first_name)
            last_name = body.get('last_name', client.last_name)
            middle_name = body.get('middle_name', client.middle_name)
            mobile_phone = body.get('mobile_phone', client.mobile_phone)
            email = body.get('email', client.email)

            client.first_name = first_name
            client.last_name = last_name
            client.middle_name = middle_name
            client.mobile_phone = mobile_phone
            client.email = email
            client.save()

            return JsonResponse({
                'success': True
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
def delete_client(request, id):
    if request.method == 'DELETE':
        client = get_object_or_404(Clients, id=id)
        client.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
# @jwt_or_csrf_required
def add_order(request):
    if request.method == 'POST':
        client_id = request.POST.get('client')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if not product or not price:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        client = get_object_or_404(Clients, id=int(client_id))
        try:
            order = Orders.objects.create(
                client=client,
                product=product,
                quantity=int(quantity),
                price=int(price),
                description=description
            )
            order.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@jwt_or_csrf_required
def get_order(request, id):
    if request.method == 'POST':
        try:
            order = get_object_or_404(Orders, id=id)
            client = order.client

            order_data = {
                'id': order.id,
                'client':{
                    'full_name': client.get_full_name(),
                    'email': client.email,
                    'mobile_phone': client.mobile_phone
                },
                'product': order.product,
                'quantity': order.quantity,
                'price': order.price,
                'total_price': order.total_price,
                'description': order.description,
                'status': order.status,
                'created_at': order.created_at.strftime("%d.%m.%Y %H:%M")
            }
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'client': order_data})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
def delete_order(request, id):
    if request.method == 'DELETE':
        order = get_object_or_404(Orders, id=id)
        order.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@jwt_or_csrf_required
def get_all_orders(request):
    if request.method == 'POST':
        try:
            start_id = int(request.POST.get('start_id', None))

            if start_id is None or not isinstance(start_id, int):
                return JsonResponse({'error': 'start_id parameter is required and must be an integer'}, status=400)

            orders = Orders.objects.filter(id__gte=start_id).order_by('id')[:20]
            clients = [order.client for order in orders]

            if not orders.exists():
                return JsonResponse({'orders': [], 'message': 'No orders found'}, status=200)


            orders_data = [
                {
                    'id': orders[i].id,
                    'client': {
                        'full_name': clients[i].get_full_name(),
                        'email': clients[i].email,
                        'mobile_phone': clients[i].mobile_phone
                    },
                    'product': orders[i].product,
                    'quantity': orders[i].quantity,
                    'price': orders[i].price,
                    'total_price': orders[i].total_price,
                    'description': orders[i].description,
                    'status': orders[i].status,
                    'created_at': orders[i].created_at.strftime("%d.%m.%Y %H:%M")
                } for i in range(orders.count())
            ]

            return JsonResponse({'orders': orders_data}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@jwt_or_csrf_required
def delete_orders(request):
    return None


def edit_order():
    return None