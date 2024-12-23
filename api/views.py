import json
import re
from datetime import timedelta
import pytz
from django.db.models.functions import Concat
from reports.models import Report
from django.contrib import messages
from django.db.models import Q, F, Value
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from clients.models import Clients
from orders.models import Orders
from .decorators import jwt_or_csrf_required
from io import BytesIO

@csrf_exempt
@jwt_or_csrf_required
def add_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        mobile_phone = request.POST.get('mobile_phone')
        email = request.POST.get('email')
        
        client_with_this_email = Clients.objects.filter(email=email).first()

        if client_with_this_email:
            return JsonResponse({'success': False, 'error': 'Email already registered.', 'id': client_with_this_email.id})

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
            try:
                messages.success(request, 'Клиент добавлен!')
            except: pass

            return JsonResponse({'success': True, 'id':client.id})
        except Exception as e:
            try:
                messages.error(request, f'Ошибка: {str(e)}')
            except: pass

            return JsonResponse({'success': False,'error': str(e)})

@csrf_exempt
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
            start_id = int(request.POST.get('start_id', 0))

            if start_id is None or not isinstance(start_id, int):
                return JsonResponse({'error': 'start_id parameter is required and must be an integer'}, status=400)

            search_filter = request.POST.get('search', '')
            search_filter_escape = re.escape(search_filter)

            # Аннотируем модель, добавляя поле full_name
            clients_query = Clients.objects.annotate(
                full_name=Concat(
                    F('last_name'),   Value(' '), F('first_name'), Value(' '), F('middle_name')
                ),
                reverse_full_name=Concat(
                     F('first_name'), Value(' '), F('last_name'),  Value(' '), F('middle_name')
                )
            )

            # Фильтруем по аннотированному полю full_name
            query = (
                Q(first_name__iregex=search_filter_escape) |
                Q(last_name__iregex=search_filter_escape) |
                Q(middle_name__iregex=search_filter_escape) |
                Q(email__iregex=search_filter_escape) |
                Q(mobile_phone__iregex=search_filter_escape) |
                Q(full_name__iregex=search_filter_escape) |
                Q(reverse_full_name__iregex=search_filter_escape)
            )
            order_by = request.POST.get('order_by', 'id')

            clients = clients_query.filter(query).order_by(order_by)[start_id:start_id+50]

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

            try:
                messages.success(request, f'Клиент изменен')
            except:
                pass
            return JsonResponse({
                'success': True,
                'id': client.id
            }, status=200)

        except Exception as e:
            try:
                messages.error(request, f'Ошибка {str(e)}')
            except:
                pass
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
def delete_client(request, id):
    if request.method == 'DELETE':
        client = get_object_or_404(Clients, id=id)
        client.delete()
        try:
            messages.success(request, f'Клиент удален')
        except:
            pass
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
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
            try:
                messages.success(request, 'Заказ добавлен')
            except:
                pass
            return JsonResponse({'success': True, 'id': order.id})
        except Exception as e:
            try:
                messages.error(request, str(e))
            except:
                pass
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
                    'id': client.id,
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
        try:
            messages.success(request, 'Заказ удален!')
        except:
            pass
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@jwt_or_csrf_required
def get_all_orders(request):
    if request.method == 'POST':
        try:
            start_id = int(request.POST.get('start_id', None))

            status = request.POST.get('status', 'Pending')

            if start_id is None or not isinstance(start_id, int):
                return JsonResponse({'error': 'start_id parameter is required and must be an integer'}, status=400)

            search_filter = request.POST.get('search', '')
            search_filter_escape = re.escape(search_filter)

            query = (
                    Q(product__iregex=search_filter_escape) |
                    Q(description__iregex=search_filter_escape)
            )

            client = request.POST.get('client_id', None)
            if client:
                query &= Q(client__id=client)
            order_by = request.POST.get('order_by', 'id')

            orders = Orders.objects.filter(status=status).filter(query).order_by(order_by)[start_id:start_id+50]
            clients = [order.client for order in orders]

            if not orders.exists():
                return JsonResponse({'orders': [], 'message': 'No orders found'}, status=200)


            orders_data = [
                {
                    'id': orders[i].id,
                    'client': {
                        'id': clients[i].id,
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

@csrf_exempt
@jwt_or_csrf_required
def edit_order(request, id):
    if request.method == 'POST':
        try:
            body = request.POST
            order = get_object_or_404(Orders, id=int(id))

            client_id = body.get('client_id', order.client.id)

            client = get_object_or_404(Clients, id=int(client_id))
            product = body.get('product', order.product)
            quantity = float(body.get('quantity', order.quantity))
            price = float(body.get('price', order.price))
            description = body.get('description', order.description)
            status = body.get('status', order.status)

            order.client = client
            order.product = product
            order.quantity = quantity
            order.price = price
            order.description = description
            order.status = status

            order.save()

            try:
                messages.success(request, f'Заказ изменен!')
            except:
                pass

            return JsonResponse({
                'success': True,
                'id': order.id
            }, status=200)

        except Exception as e:
            try:
                messages.error(request, f'Ошибка: {str(e)}')
            except:
                pass
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@jwt_or_csrf_required
def add_report(request):
    if request.method == 'POST':
        try:
            period = request.POST.get('period', 'month')

            period_days = {
                'week': 7,
                'month': 30,
                'year': 365,
            }

            time_ago = timezone.now() - timedelta(days=period_days[period])

            # Заказы за выбранный период
            orders = Orders.objects.filter(created_at__gte=time_ago)
            order_count = orders.count()
            order_total_sum = sum([float(order.total_price) for order in orders])
            order_avg_sum = order_total_sum / order_count if order_count > 0 else 0
            completed_orders_count = orders.filter(status='Completed').count()

            # Клиенты, добавленные за выбранный период
            clients = Clients.objects.filter(added_at__gte=time_ago)

            # Создаем отчет
            report = Report(
                period=period,
                new_orders_count=order_count,
                new_clients_count=clients.count(),
                total_orders_sum=order_total_sum,
                avg_order_sum=order_avg_sum,
                completed_orders_count=completed_orders_count,
            )
            report.save()
            try:
                messages.success(request, f'Отчет создан')
            except:
                pass
            return JsonResponse({'success': True, 'id': report.id})

        except Exception as e:
            try:
                messages.error(request, f'Ошибка: {str(e)}')
            except:
                pass
            return JsonResponse({'success': False, 'error': str(e)})

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_txt(report):
    txt_buffer = BytesIO()

    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = report.date_created.astimezone(moscow_tz)

    months_russian = [
        'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
        'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'
    ]
    formatted_date = f"{moscow_time.day} {months_russian[moscow_time.month - 1]} {moscow_time.year} года, {moscow_time.strftime('%H:%M')}"

    txt_content = (
        f"Отчет за период: {report.get_period_display()}\n"
        f"Дата создания: {formatted_date}\n"
        f"Кол-во новых заказов: {report.new_orders_count}\n"
        f"Кол-во новых клиентов: {report.new_clients_count}\n"
        f"Сумма новых заказов: {report.total_orders_sum}\n"
        f"Средняя сумма заказов: {report.avg_order_sum}\n"
        f"Кол-во выполненных заказов: {report.completed_orders_count}\n\n"
    )

    txt_buffer.write(txt_content.encode('utf-8'))
    txt_buffer.seek(0)
    return txt_buffer

@csrf_exempt
def get_report(request, id):
    try:
        report = Report.objects.get(id=id)

        txt_buffer = generate_txt(report)

        response = HttpResponse(txt_buffer, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=report_{id}.txt'
        return response
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)

@csrf_exempt
@jwt_or_csrf_required
def get_all_reports(request):
    reports = Report.objects.order_by('-id').all()
    reports_data = []


    for report in reports:
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = report.date_created.astimezone(moscow_tz)

        months_russian = [
            'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
            'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'
        ]
        formatted_date = f"{moscow_time.day} {months_russian[moscow_time.month - 1]} {moscow_time.year} года, {moscow_time.strftime('%H:%M')}"


        reports_data.append({
            'id': report.id,
            'period': report.period,
            'new_orders_count': report.new_orders_count,
            'new_clients_count': report.new_clients_count,
            'total_orders_sum': str(report.total_orders_sum),
            'avg_order_sum': str(report.avg_order_sum),
            'completed_orders_count': report.completed_orders_count,
            'date_created':formatted_date
        })

    return JsonResponse({'reports': reports_data})

@csrf_exempt
@jwt_or_csrf_required
def get_report(request, id):
    try:
        report = Report.objects.get(id=id)

        txt_buffer = generate_txt(report)

        response = HttpResponse(txt_buffer, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename=report_{id}.txt'
        return response
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
