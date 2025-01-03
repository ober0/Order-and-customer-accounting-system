from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from clients.models import Clients
from main.functions import addUserData
from orders.models import Orders
from main.decorators import login_required_custom

@login_required_custom
def orders(request):
    context = {}
    context = addUserData(request, context)
    client_id = request.GET.get('client_id')
    if client_id:
        context['client_id'] = client_id


    return render(request, 'orders/orders.html', context)

@login_required_custom
def order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    get_object_or_404(Orders, id=int(id))

    return render(request, 'orders/order.html', context)

@login_required_custom
def edit_order(request, id):
    context = {'order_id': id}
    context = addUserData(request, context)

    get_object_or_404(Orders, id=int(id))

    return render(request, 'orders/edit_order.html', context)

@login_required_custom
def add_order(request):
    context = {}
    context = addUserData(request, context)

    client_select = request.GET.get('client_select')
    if client_select:
        context['client_select'] = client_select
        client = get_object_or_404(Clients, id=int(client_select))
        context['client_select_text'] = client.get_full_name()


    return render(request, 'orders/add_order.html', context)