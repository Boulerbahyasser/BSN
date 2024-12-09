import os

from django.http import JsonResponse
from django.shortcuts import render
from xhtml2pdf import pisa
from datetime import datetime
from livre.models import Livre, LivrePhysique
from transaction.models import Transaction, Facture
from utilisateur.models import Utilisateur


def buy_physical_book(request, book_id):

    user_id = 1
    user = Utilisateur.objects.get(id=user_id)
    book = LivrePhysique.objects.get(livre_ptr_id=book_id)
    if book.stock_vente != book.vendus:
        transaction = Transaction.objects.create(utilisateur_id=user_id,livre_id = book_id,type = 'achat',montant = book.prix_vente)
        book.vendus+=1
        book.save()
        generate_facture(book, transaction, user)
        return JsonResponse({'message': 'Transaction is done'}, status=201)
    else:
        return JsonResponse({'message': 'Book is out of stock'}, status=400)



def generate_facture(book,transaction,user):
    facture = Facture.objects.create(montant=book.prix_vente, transaction_id=transaction.id)
    pdf_facture_path =generate_facture_pdf(facture.id,
                                           f'{user.first_name} {user.last_name}',
                                           transaction.type,transaction.montant,book.titre)
    facture.path_facture_pdf=pdf_facture_path
    facture.save()







def generate_facture_pdf(facture_id, nom_client, type_transaction, montant, nom_livre):

    pdf_directory = os.path.join("media", "factures")
    os.makedirs(pdf_directory, exist_ok=True)  # Ensure the directory exists

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f"facture_{facture_id}_{nom_client}_{timestamp}.pdf"
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
                margin-top: 30px;
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
            </div>

            <div class="transaction">
                <p><strong>Transaction ID:</strong> {facture_id}</p>
                <p><strong>Date de la transaction:</strong> {datetime.now().strftime('%d %B %Y')}</p>
            </div>

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