from typing import Callable

from django.urls import path
from . import views

urlpatterns: list[Callable] = [
    path('forum/', views.forum_view, name='forum'),
]
