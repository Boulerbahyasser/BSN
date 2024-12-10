from django.urls import path, include

from .Controller import *
urlpatterns = [
    path('afficher/livre/', show_all_transaction_of_user, name='show_all_transaction_of_user'),
    path('acheter/livre/physique/<int:book_id>/', buy_physical_book, name='buy_physical_book'),

    path('acheter/livre/numerique/<int:book_id>/', buy_numeric_book, name='buy_numeric_book'),
    path('emprunter/livre/physique/<int:book_id>/<int:days>/', borrow_book, name='borrow_book'),
    path('retourner/livre/physique/<int:book_id>/', return_book, name='return_book'),
]

