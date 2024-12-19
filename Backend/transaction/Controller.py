import os


from django.http import JsonResponse

from xhtml2pdf import pisa
from datetime import datetime, timedelta
from livre.models import Livre, LivrePhysique, LivreNumerique
from transaction.models import Transaction, Facture, TransactionEmprunt
from utilisateur.models import Utilisateur
from notification.Controller import *
def show_all_transactions_of_user(request):
    user_id = request.user.id
    # user_id = 2
    transactions = Transaction.objects.filter(utilisateur_id=user_id)
    return JsonResponse(
        Transaction.serialize_to_json(transactions),
        safe=False,status=200
    )
def show_all_borrowing_transactions_of_user(request):
    user_id = request.user.id
    # user_id = 2
    transactions = TransactionEmprunt.objects.filter(utilisateur_id=user_id)
    return JsonResponse(
        TransactionEmprunt.serialize_to_json(transactions),
        safe=False, status=200
    )
def show_all_buying_transactions_of_user(request):
    user_id = request.user.id
    # user_id = 2
    transactions = Transaction.objects.filter(utilisateur_id=user_id,type='achat')
    return JsonResponse(
        Transaction.serialize_to_json(transactions),
        safe=False, status=200
    )

def show_all_related_transactions_of_user_books(request):
    user_id = request.user.id
    # user_id = 1
    queryset = Transaction.objects.select_related('livre').filter(
        livre__utilisateur_id=user_id
    ).values(*Transaction.get_attributes(), 'livre__titre')
    return JsonResponse(
        list(queryset),
        safe=False,
        status=200
    )




def buy_physical_book(request, book_id):
    user_id = request.user.id
    # user_id = 3
    user = Utilisateur.objects.get(id=user_id)
    book = LivrePhysique.objects.get(livre_ptr_id=book_id)
    if book.stock_vente != book.vendus:
        transaction = Transaction.objects.create(utilisateur_id=user_id,livre_id = book_id,type_livre='physique',type = 'achat',montant = book.prix_vente)
        book.vendus+=1
        book.save()
        pdf_facture_path = generate_facture(book, transaction, user,'Physique')
        notify_buyer(user_id,book.titre,pdf_facture_path)
        notify_seller(book.utilisateur_id,book.titre,transaction.id,
                      'physique',f'{user.first_name} {user.last_name}')
        return JsonResponse({"facture": pdf_facture_path}, status=201)
    else:
        return JsonResponse({'message': 'Book is out of stock'}, status=400)
def buy_numeric_book(request, book_id):
    user_id = request.user.id
    # user_id = 1
    user = Utilisateur.objects.get(id=user_id)
    book = LivreNumerique.objects.get(livre_ptr_id=book_id)
    transaction = Transaction.objects.create(utilisateur_id=user_id,type_livre='numerique',livre_id = book_id,type = 'achat',montant = book.prix_vente)
    pdf_facture_path = generate_facture(book, transaction, user,'Numerique')
    notify_buyer(user_id,book.titre, pdf_facture_path)
    notify_seller(book.utilisateur_id, book.titre, transaction.id,
                  'numerique',f'{user.first_name} {user.last_name}')
    return JsonResponse({'livre':book.path_livre_pdf,"facture": pdf_facture_path}, status=201)

def borrow_book(request, book_id,days):
    user_id = request.user.id
    # user_id = 2
    user = Utilisateur.objects.get(id=user_id)
    book = LivrePhysique.objects.get(livre_ptr_id=book_id)
    count = (
        TransactionEmprunt.objects.filter(
            utilisateur_id=user_id,
            dateRetour__isnull=True
        )
        .count()
    )
    # transaction = TransactionEmprunt.objects.filter(utilisateur_id=user_id, livre_id=book_id, dateRetour=None).first()
    # if transaction:
    #     return JsonResponse({'message': 'You cannot borrow the same book until you return the first one.'}, status=400)

    if count<3:
        if book.stock_emprunt != book.empruntes:
            date_retour_prevu =  datetime.now().date() + timedelta(days=days)
            transaction = TransactionEmprunt.objects.create(utilisateur_id=user_id, livre_id=book_id, type_livre='physique',
                                                     type='emprunt', montant=book.prix_vente,dateRetourPrevue=date_retour_prevu,dateRetour=None)
            book.empruntes += 1
            book.save()
            pdf_facture_path = generate_facture(book, transaction, user, 'Physique',date_retour_prevu)
            notify_borrower(user_id,book.titre,date_retour_prevu,pdf_facture_path)
            notify_owner_on_borrow(book.utilisateur_id,book.titre,
                                   transaction.id, f'{user.first_name} {user.last_name}',date_retour_prevu)
            return JsonResponse({"facture": pdf_facture_path}, status=201)
        else:
            return JsonResponse({'message': 'Book is out of stock'}, status=400)
    else:
        return JsonResponse({'message': 'You can barrow only 3 books in one row'}, status=400)

def return_book(request, book_id):
    user_id = request.user.id
    # user_id = 2
    user = Utilisateur.objects.get(id=user_id)
    transaction = TransactionEmprunt.objects.filter(utilisateur_id=user_id,livre_id=book_id, dateRetour=None).first()
    if transaction is None:
        return JsonResponse({'message': 'Transaction is closed or no transaction concern this book'}, status=400)
    now = datetime.now().date()
    transaction.dateRetour = now
    transaction.save()
    book = LivrePhysique.objects.get(livre_ptr_id=book_id)
    book.empruntes -= 1
    book.save()
    if now > transaction.dateRetourPrevue:
        livre_taux_amende = LivrePhysique.objects.get(livre_ptr_id=book_id).taux_amende

        book_price = book.prix_vente
        days_late = (now-transaction.dateRetourPrevue).days
        amende = book_price*livre_taux_amende*days_late
        fine_pdf = generate_fine_pdf(f'{user.first_name} {user.last_name}',
                                     book.titre,transaction.dateRetour,transaction.dateRetourPrevue,amende)
        notify_borrower_on_fine(user_id,book.titre,amende,transaction.id,fine_pdf)
        notify_owner_on_book_return(book.utilisateur_id,book.titre,f'{user.first_name} {user.last_name}',
                                    transaction.id,amende)
        return JsonResponse({'fine_pdf': fine_pdf}, status=200)
    else:
        notify_owner_on_book_return(book.utilisateur_id, book.titre, f'{user.first_name} {user.last_name}',
                                    transaction.id)
        return JsonResponse({'message': 'The book has been returned successfully'}, status=200)


def generate_facture(book,transaction,user,type_livre,date_retour=None):
    facture = Facture.objects.create(montant=book.prix_vente, transaction_id=transaction.id)
    pdf_facture_path =generate_facture_pdf(facture.id,
                                           f'{user.first_name} {user.last_name}',
                                           transaction.type,transaction.montant,book.titre,type_livre,date_retour)
    facture.path_facture_pdf=pdf_facture_path
    facture.save()
    return pdf_facture_path


def generate_facture_pdf(facture_id, nom_client, type_transaction, montant, nom_livre,type_livre,date_retour=None):
    pdf_directory = os.path.join("media", "factures")
    os.makedirs(pdf_directory, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f"facture_{facture_id}_{nom_client.replace(" ", "_")}_{timestamp}.pdf"
    pdf_path = os.path.join(pdf_directory, pdf_filename)

    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                background-color: #e9f0f7;
            }}
            .container {{
                width: 80%;
                max-width: 900px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin: 30px auto;
                box-sizing: border-box;
            }}
            h1 {{
                color: #003366;
                font-size: 32px;
                margin-bottom: 10px;
                text-align: center;
            }}
            h2 {{
                color: #003366;
                font-size: 20px;
                margin-top: 20px;
                font-weight: bold;
                border-bottom: 2px solid #003366;
                padding-bottom: 8px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .logo {{
                font-size: 22px;
                font-weight: bold;
                color: #003366;
            }}
            .date {{
                font-size: 14px;
                color: #555;
                font-style: italic;
            }}
            .info {{
                margin-top: 20px;
                font-size: 16px;
                background-color: #f9fafb;
                padding: 15px;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            }}
            .info p {{
                margin: 8px 0;
            }}
            .info strong {{
                color: #003366;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #777;
                text-align: center;
                padding: 10px 0;
                border-top: 1px solid #f0f0f0;
            }}
            .footer p {{
                margin: 5px 0;
            }}
            .transaction {{
                background-color: #f7f9fc;
                padding: 15px;
                margin-top: 20px;
                border-radius: 8px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            }}
            .transaction p {{
                font-size: 16px;
                margin-bottom: 8px;
            }}
            .transaction p strong {{
                color: #003366;
                font-weight: bold;
            }}
            .warning {{
                margin-top: 30px;
                color: #D32F2F;
                font-size: 14px;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border: 1px solid #D32F2F;
                border-radius: 5px;
                background-color: #FFF5F5;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">Book Social Network</div>
                <div class="date">{datetime.now().strftime('%d %B %Y')}</div>
            </div>
            <h1>Facture {facture_id}</h1>

            <h2>Détails de la transaction</h2>
            <div class="info">
                <p><strong>Nom du client :</strong> {nom_client}</p>
                <p><strong>Type de transaction :</strong> {type_transaction.capitalize()}</p>
                <p><strong>Montant :</strong> {montant} €</p>
                <p><strong>Nom du livre :</strong> {nom_livre}</p>
                <p><strong>Type du livre :</strong> {type_livre}</p>
                {f"<p><strong>Date limite de retour du livre :</strong> {date_retour}</p>" if date_retour else ""}
            </div>

            <div class="transaction">
                <p><strong>Transaction ID:</strong> {facture_id}</p>
            </div>
            {f"""<div class="warning">
                <p><strong>Attention :</strong> En cas de non-respect de la date limite de retour, une amende sera appliquée.</p>
            </div>""" if date_retour else ""}

            <div class="footer">
                <p>Merci pour votre confiance.</p>
                <p>Facture générée par BSN.</p>
            </div>
        </div>
    </body>
    </html>
    """

    with open(pdf_path, "w+b") as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

    return f"/media/factures/{pdf_filename}"


def generate_fine_pdf(nom_client, nom_livre, dateRetour, dateRetourPrevu, amende):
    pdf_directory = os.path.join("media", "amendes")
    os.makedirs(pdf_directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f"fine_{nom_client.replace(' ', '_')}_{timestamp}.pdf"
    pdf_path = os.path.join(pdf_directory, pdf_filename)

    # HTML content with styling
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                background-color: #f7f9fc;
            }}
             .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .header p {{
                margin: 5px 0;
            }}
            .logo {{
                font-size: 22px;
                font-weight: bold;
                color: #003366;
            }}
            .container {{
                width: 80%;
                max-width: 800px;
                margin: 30px auto;
                padding: 20px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #D32F2F;
                text-align: center;
                font-size: 28px;
                margin-bottom: 20px;
            }}
            .details {{
                font-size: 16px;
                margin-bottom: 20px;
                line-height: 1.6;
            }}
            .details p {{
                margin: 10px 0;
            }}
            .details strong {{
                color: #003366;
            }}
            .amount {{
                font-size: 18px;
                font-weight: bold;
                color: #D32F2F;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 14px;
                text-align: center;
                color: #555;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
                <div class="logo">Book Social Network</div>
            </div>
        <div class="container">
            <h1>Facture d'Amende</h1>
            <div class="details">
                <p><strong>Nom du Client :</strong> {nom_client}</p>
                <p><strong>Nom du Livre :</strong> {nom_livre}</p>
                <p><strong>Date de Retour :</strong> {dateRetour.strftime('%d %B %Y')}</p>
                <p><strong>Date de Retour Prévue :</strong> {dateRetourPrevu.strftime('%d %B %Y')}</p>
            </div>
            <div class="amount">
                <p>Montant de l'Amende : <strong>{amende:.2f} €</strong></p>
            </div>
            <div class="footer">
                <p>Merci de bien vouloir régler cette amende.</p>
                <p>Facture générée par BSN.</p>
            </div>
        </div>
    </body>
    </html>
    """
    # Generate the PDF
    with open(pdf_path, "w+b") as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)

    return f"/media/amendes/{pdf_filename}"


