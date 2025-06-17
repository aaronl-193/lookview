from typing import Callable

from django.urls import path
from . import views

urlpatterns: list[Callable] = [
    path('film/<str:film_id>/', views.film_detail_view, name='films'),
    path('catalog/', views.catalog_view, name='catalog'),
]
