from django.urls import path, include

from .Controller import *

urlpatterns = [
    path('acheter/livre/physique/<int:book_id>/', buy_physical_book, name='buy_physical_book'),
]