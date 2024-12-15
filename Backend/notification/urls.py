from django.urls import path, include
from . import Controller
from .Controller import show_all_notifications, change_notification_status

urlpatterns = [
    path('show/notifications/', show_all_notifications, name='show_all_notifications'),
    path('mark/as/read/<int:notification_id>/', change_notification_status, name='change_notification_status'),
]