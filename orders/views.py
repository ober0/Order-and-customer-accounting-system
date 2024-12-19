from django.contrib import messages
from django.shortcuts import render
from main.functions import addUserData

def orders(request):
    context = {}
    context = addUserData(request, context)

    msg = request.GET.get('msg', None)
    if msg == 'successadd':
        messages.success(request, 'Успешно!')
    elif msg == 'erroradd':
        messages.error(request, 'Ошибка добавления')
    return render(request, 'orders/orders.html', context)


def order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    return render(request, 'orders/order.html', context)


def edit_order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    return render(request, 'orders/edit_order.html', context)