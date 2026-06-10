# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            # login(request, user)
            # # Redirect based on user type
            # if username == 'tr@n1n85ec1':
            #     return redirect('dashboard:index')  # dashboard 1
            # # elif username == 'admin2':
            # #     return redirect('search:index')  # dashboard 2
            # else:
            #     logout(request)
            #     messages.error(request, 'Unauthorized access.')
            #     return redirect('accounts:login')
            login(request, user)
            return redirect('dashboard:index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def custom_logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')
