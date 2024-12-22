from django.shortcuts import render

from main.decorators import login_required_custom
from main.functions import addUserData


# Create your views here.
@login_required_custom
def reports(request):
    context = {}
    context = addUserData(request, context)

    return render(request, 'reports/reports.html', context)