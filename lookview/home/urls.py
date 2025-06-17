from typing import Callable

from django.urls import path
from . import views

urlpatterns: list[Callable] = [
    path('', views.homepage_view, name='home'),
]
