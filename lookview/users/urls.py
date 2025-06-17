from django.urls import path
from . import views

urlpatterns: list[path] = [
    path('user/<str:username>/', views.user_page_view, name='users'),
    path('user/<str:username>/view', views.user_outside_view, name='users_outside'),
]
