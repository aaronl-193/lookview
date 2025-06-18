from django import forms
from django import http
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import login, logout, authenticate, models

from users.models import SiteUser
from .forms import SignupForm, LoginForm

def signup_view(request: http.HttpRequest, *args, **kwargs) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')
    context = {
        "confirmation_failed": False
    }
    if request.POST:
        username: str = request.POST.get("username")
        email: str = request.POST.get("email")
        password: str = request.POST.get("password")
        confirmation_pass: str = request.POST.get("confirm-password")
        if password != confirmation_pass:
            context["confirmation_failed"] = True
        elif username in [user.username for user in models.User.objects.all()]:
            context["confirmation_failed"] = True
        else:
            user: models.User = models.User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            SiteUser.objects.create_site_user(user)
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', context)

def login_view(request: http.HttpRequest, *args, **kwargs) -> HttpResponse:
    context = {
        "login_failed": False
    }
    if request.user.is_authenticated:
        return redirect('home')
    if request.POST:
        username: str = request.POST.get("username")
        password: str = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        context["login_failed"] = True
    return render(request, 'login.html', context)

def logout_view(request: http.HttpRequest, *args, **kwargs) -> HttpResponse:
    logout(request)
    return redirect('home')
