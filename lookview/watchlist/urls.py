from django.urls import path
from . import views

urlpatterns: list[path] = [
    path('user/<str:username>/watchlist', views.watchlist_view, name='watchlist'),
]
