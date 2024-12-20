from django.shortcuts import render

from main.decorators import login_required_custom


# Create your views here.
@login_required_custom
def reports(request):
    return render(request, 'reports/reports.html')