from typing import Callable

from django.urls import path
from . import views

urlpatterns: list[Callable] = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
