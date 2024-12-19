from django.http import JsonResponse
from django.shortcuts import render

from .decorators import login_required_custom
from .functions import addUserData


@login_required_custom
def main(request):
    context = {}
    context = addUserData(request, context)

    return render(request, 'main/index.html', context=context)