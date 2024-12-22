from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from clients.models import Clients
from api.decorators import jwt_or_csrf_required
from main.decorators import login_required_custom
from main.functions import addUserData


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
                staff = request.POST.get('staff', 'off')
                print(staff)

                user = User(first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    username=request.POST.get('username'),
                    email=request.POST.get('email'),
                    is_staff=True if staff == 'on' else False)
                user.set_password(request.POST.get('password'))

                user.save()


                messages.success(request, 'Успех!')
                return JsonResponse({'success': True})
            except Exception as e:
                messages.error(request, str(e))
                return JsonResponse({'success': False})
        elif request.method == 'GET':
            context = {}
            context = addUserData(request, context)

            return render(request, 'login/new_user.html', context)
    messages.error(request, 'Недостаточно прав')
    return redirect('main')

def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('login')

@csrf_exempt
@jwt_or_csrf_required
def edit(request):
    if request.method == 'POST':
        try:
            user = request.user

            first_name = request.POST.get('first_name', user.first_name)
            last_name = request.POST.get('last_name', user.last_name)
            email = request.POST.get('email', user.email)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            user.save()

            messages.success(request, 'Успешно')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, 'Произошла ошибка')
            return JsonResponse({'success': False})
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
@login_required_custom
@jwt_or_csrf_required
def admin_edit(request,id):
    if request.method == 'POST':
        if request.user.is_staff or request.user.is_superuser:
            if request.method == 'POST':
                try:
                    user = User.objects.get(id=id)

                    first_name = request.POST.get('first_name', user.first_name)
                    last_name = request.POST.get('last_name', user.last_name)
                    email = request.POST.get('email', user.email)

                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email

                    user.save()

                    messages.success(request, 'Успешно')
                    return JsonResponse({'success': True})
                except Exception as e:
                    messages.error(request, 'Произошла ошибка')
                    return JsonResponse({'success': False})
        messages.error(request, 'Недостаточно прав')
        return redirect('main')
    return JsonResponse({'error': 'Method not allowed'}, status=405)