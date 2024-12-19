from django.shortcuts import render
from main.functions import addUserData

def orders(request):
    context = {}
    context = addUserData(request, context)

    return render(request, 'orders/orders.html', context)


def order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    return render(request, 'orders/order.html', context)