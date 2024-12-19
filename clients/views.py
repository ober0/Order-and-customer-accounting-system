from django.shortcuts import render
from main.functions import addUserData
# Create your views here.
def clientsView(request):
    context = {}
    context = addUserData(request, context)

    return render(request, 'clients/clients.html', context)

def clientView(request, id):
    context = {'client_id': id}
    context = addUserData(request, context)

    return render(request, 'clients/client.html', context)
