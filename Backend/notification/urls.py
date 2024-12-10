from django.urls import path, include
from . import Controller
from .Controller import show_all_notifications

urlpatterns = [
    path('show/notifications/', show_all_notifications, name='show_all_notifications'),
]