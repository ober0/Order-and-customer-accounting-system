from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from main.functions import addUserData
from orders.models import Orders


def orders(request):
    context = {}
    context = addUserData(request, context)
    client_id = request.GET.get('client_id')
    if client_id:
        context['client_id'] = client_id


    return render(request, 'orders/orders.html', context)


def order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    get_object_or_404(Orders, id=int(id))

    return render(request, 'orders/order.html', context)


def edit_order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    get_object_or_404(Orders, id=int(id))

    return render(request, 'orders/edit_order.html', context)


def add_order(request):
    context = {}
    context = addUserData(request, context)


    return render(request, 'orders/add_order.html', context)