from django.urls import path, include
from . import Controller
from .Controller import *

urlpatterns = [
    path('show/notifications/', show_all_notifications, name='show_all_notifications'),
    path('show/notification/<int:notification_id>/', show_notification, name='show_notification'),
]