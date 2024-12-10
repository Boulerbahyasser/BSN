from django.urls import path, include

from .Controller import *
urlpatterns = [
    path('afficher/livre/', show_all_transactions_of_user, name='show_all_transactions_of_user'),
    path('afficher/livre/emprunt/', show_all_borrowing_transactions_of_user, name='show_all_borrowing_transactions_of_user'),
    path('acheter/livre/physique/<int:book_id>/', buy_physical_book, name='buy_physical_book'),

    path('acheter/livre/numerique/<int:book_id>/', buy_numeric_book, name='buy_numeric_book'),
    path('emprunter/livre/physique/<int:book_id>/<int:days>/', borrow_book, name='borrow_book'),
    path('retourner/livre/physique/<int:book_id>/', return_book, name='return_book'),
]

