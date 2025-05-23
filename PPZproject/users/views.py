from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm

def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('songs:index')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {
        'title': 'Music Django - Вхід',
        'form': form,
    })

def user_registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('songs:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {
        'title': 'Music Django - Реєстрація',
        'form': form,
    })

@login_required
def user_logout_view(request):
    logout(request)
    return redirect('songs:index')
