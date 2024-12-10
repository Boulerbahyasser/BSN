from django.http import JsonResponse
from django.shortcuts import render

from notification.models import Notification


def show_all_notifications(request):
    # user_id = request.user.id
    user_id = 2
    notifications = Notification.objects.filter(utilisateur_id=user_id)
    return JsonResponse(
        Notification.serialize_to_json(notifications),
        safe=False,
        status=200
    )

# def create_notification():
#     Notification.objects.create(utilisateur_id=user_id,contenu=contenu,type=notif_type,attachement=attachement)


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

def notify_borrower(user_id, book_title, return_date,facture_pdf):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Votre demande d'emprunt pour le livre '{book_title}' a été acceptée avec succès.\n"
            f"Veuillez noter que ce livre doit être retourné avant le {return_date}.\n"
            f"Pour plus de détails, vous pouvez télécharger la facture ci-jointe."
        ),
        type='emprunt_emprunteur',
        attachement=facture_pdf

    )

def notify_owner_on_borrow(user_id, book_title, transaction_id, borrower_name, return_date):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Le livre '{book_title}' a été emprunté par {borrower_name}.\n"
            f"La date de retour prévue est le {return_date}.\n"
            f"Vous pouvez consulter les détails de la transaction (ID: {transaction_id}) dans votre espace personnel."
        ),
        type='emprunt_proprietaire'
    )


def notify_owner_on_book_return(user_id, titre_livre, borrower_name, transaction_id, amende=None):
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
        utilisateur_id=user_id,
        contenu=contenu,
        type='retour_livre'
    )

def notify_borrower_on_fine(user_id, livre_titre, amende, transaction_id, facture_path):
    Notification.objects.create(
        utilisateur_id=user_id,
        contenu=(
            f"Bonjour, vous avez été informé d'un retard pour le livre '{livre_titre}'.\n"
            f"Une amende de {amende:.2f} € a été appliquée en raison du retard.\n"
            f"Vous pouvez consulter la facture détaillée ci-jointe (ID de transaction : {transaction_id})."
        ),
        type='amende',
        attachement=facture_path
    )