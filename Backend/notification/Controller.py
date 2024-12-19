from django.http import JsonResponse
from django.shortcuts import render

from notification.models import Notification


def show_all_notifications(request):
    user_id = request.user.id
    # user_id = 2
    notifications = Notification.objects.filter(utilisateur_id=user_id)
    return JsonResponse(
        Notification.serialize_to_json(notifications),
        safe=False,
        status=200
    )
def show_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read_status = True
    notification.save()

    return JsonResponse(
        notification.to_dict(),
    )


def notify_buyer(user_id,book_title,facture_pdf):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=f"Votre transaction pour l'achat du livre '{book_title}' a été effectuée avec succès.\n"
        f"Pour plus de détails, vous pouvez télécharger la facture ci-jointe.",
        type='achat',
        attachement=facture_pdf
    )

def notify_seller(user_id, book_title, transaction_id, livre_type,buyer_name):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Félicitations ! Votre livre '{book_title}' (version {livre_type}) a été vendu avec succès à {buyer_name}.\n"
            f"Vous pouvez consulter les détails de la transaction (ID: {transaction_id}) dans votre espace personnel."
        ),
        type='vente'
    )

def notify_borrower(borrower_id, book_title, return_date,facture_pdf):
    Notification.objects.create(
        utilisateur_id=borrower_id,
        contenu=(
            f"Votre demande d'emprunt pour le livre '{book_title}' a été acceptée avec succès.\n"
            f"Veuillez noter que ce livre doit être retourné avant le {return_date}.\n"
            f"Pour plus de détails, vous pouvez télécharger la facture ci-jointe."
        ),
        type='emprunt_emprunteur',
        attachement=facture_pdf

    )

def notify_owner_on_borrow(owner_id, book_title, transaction_id, borrower_name, return_date):
    Notification.objects.create(
        utilisateur_id=owner_id,
        contenu=(
            f"Le livre '{book_title}' a été emprunté par {borrower_name}.\n"
            f"La date de retour prévue est le {return_date}.\n"
            f"Vous pouvez consulter les détails de la transaction (ID: {transaction_id}) dans votre espace personnel."
        ),
        type='emprunt_proprietaire'
    )


def notify_owner_on_book_return(owner_id, titre_livre, borrower_name, transaction_id, amende=None):
    if amende:
        contenu = (
            f"Le livre '{titre_livre}' a été retourné par {borrower_name}.\n"
            f"Un retard a été constaté, et une amende de {amende:.2f} € a été appliquée au lecteur.\n"
            f"Les détails de la transaction (ID : {transaction_id}) sont disponibles dans votre espace personnel."
        )
    else:
        contenu = (
            f"Le livre '{titre_livre}' a été retourné par {borrower_name}.\n"
            f"Vous pouvez consulter les détails de la transaction (ID : {transaction_id}) dans votre espace personnel.\n"
            f"Merci d'avoir permis cet emprunt !"
        )

    Notification.objects.create(
        utilisateur_id=owner_id,
        contenu=contenu,
        type='retour_livre'
    )

def notify_borrower_on_fine(borrower_id, book_title, amende, transaction_id, facture_path):
    Notification.objects.create(
        utilisateur_id=borrower_id,
        contenu=(
            f"Bonjour, vous avez été informé d'un retard pour le livre '{book_title}'.\n"
            f"Une amende de {amende:.2f} € a été appliquée en raison du retard.\n"
            f"Vous pouvez consulter la facture détaillée ci-jointe (ID de transaction : {transaction_id})."
        ),
        type='amende',
        attachement=facture_path
    )

def notify_seller_on_stock_empty(seller_id, book_title):
    Notification.objects.create(
        utilisateur_id=seller_id,
        contenu=(
            f"Bonjour, votre stock de livre '{book_title}' est maintenant vide.\n"
            f"Nous vous recommandons de réapprovisionner ce livre dès que possible, "
            f"ou de supprimer ce livre de votre inventaire."
        ),
        type='stock_vide'
    )

def notify_user_on_book_arrival(user_id, book_titre,stock_type):
    """
    Notifies a user when a book they requested is back in stock.
    - stock_type (str): The type of stock the book is available in. Can be:
        - 'emprunt': The book is available for borrowing.
        - 'achat' : The book is available for purchase.
    """
    if stock_type == 'emprunt':
        stock_message = "disponible pour l'emprunt."
    elif stock_type == 'achat':
        stock_message = "disponible à la vente."
    else:
        raise Exception("Invalid stock_type. Expected 'emprunt' or 'achat'.")

    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Bonjour, le livre '{book_titre}' que vous avez demandé est maintenant {stock_message}\n"
            f"Vous pouvez le réserver ou l'acheter/emprunter dès que possible."
        ),
        type='arrivee_livre',
        attachement=None
    )

def notify_user_on_comment(user_id,book_title):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Bonjour, un nouveau commentaire a été posté sur le livre '{book_title}'.\n"
            f"Nous vous invitons à le consulter pour découvrir l'avis d'autres lecteurs."
        ),
        type='commentaire_livre',
        attachement=None
    )