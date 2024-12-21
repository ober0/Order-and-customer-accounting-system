from django.shortcuts import render, get_object_or_404
from main.decorators import login_required_custom
from clients.models import Clients
from main.functions import addUserData
# Create your views here.

@login_required_custom
def clientsView(request):
    context = {}
    context = addUserData(request, context)

    return render(request, 'clients/clients.html', context)


@login_required_custom
def clientView(request, id):
    context = {'client_id': id}
    context = addUserData(request, context)

    get_object_or_404(Clients, id=int(id))

    return render(request, 'clients/client.html', context)

@login_required_custom
def edit_client(request, id):
    context = {'client_id': id}
    context = addUserData(request, context)

    get_object_or_404(Clients, id=int(id))

    return render(request, 'clients/edit_client.html', context)

@login_required_custom
def add_client(request):
    context = {'client_id': id}
    context = addUserData(request, context)

    return render(request, 'clients/add_client.html', context)