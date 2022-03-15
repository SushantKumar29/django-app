from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm


def login_view(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('/pictures')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/pictures')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login')
    return render(request, 'accounts/logout.html', {})


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)
