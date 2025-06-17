from typing import Callable

from django.urls import path
from . import views

urlpatterns: list[Callable] = [
    path('film/<str:film_id>/review', views.review_film_view, name='review_film'),
]
