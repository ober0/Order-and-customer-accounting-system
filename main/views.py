from django.http import JsonResponse
from .decorators import login_required_custom



@login_required_custom
def main(request):
    return JsonResponse({})