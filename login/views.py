from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from clients.models import Clients
from api.decorators import jwt_or_csrf_required
from main.decorators import login_required_custom

def login(request):
    if request.method == 'GET':
        next = request.GET.get('next', '')
        return render(request, 'login/login.html', {'next': next})

    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        next = request.POST.get('next')
        if next is None or next == '':
            next = 'main'

        user = authenticate(request, email=login, password=password)
        if not user:
            user = authenticate(request, username=login, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Успешный вход в аккаунт')
            return redirect(next)
        else:
            messages.error(request, 'Неверный логин или пароль')
            return render(request, 'login/login.html', {'error':True, 'next': next})

@csrf_exempt
@login_required_custom
@jwt_or_csrf_required
def new_user(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            try:
                client = Clients.objects.create(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    middle_name=request.POST.get('middle_name'),
                    email=request.POST.get('email'),
                    mobile_phone=request.POST.get('mobile_phone'),
                )

                messages.success(request, 'Успех!')
                return JsonResponse({'success': True})
            except Exception as e:
                messages.error(request, str(e))
                return JsonResponse({'success': False})
        elif request.method == 'GET':
            return render(request, 'login/new_user.html')
    messages.error(request, 'Недостаточно прав')
    return redirect('main')


def logout(request):
    auth_logout(request)
    return redirect('login')


def edit(request):
    return None


def admin_edit(request):
    return None