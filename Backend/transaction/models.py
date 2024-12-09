from django.db import models



class Transaction(models.Model):
    TYPE_TRANSACTION_CHOICES = [
        ('achat', 'Achat'),
        ('emprunt', 'Emprunt'),
    ]

    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name="transactions")
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_TRANSACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_livre = models.CharField(default="")
    class Meta:
        db_table = 'transaction'

class TransactionEmprunt(Transaction):
    dateRetour = models.DateField(null=True, blank=True)
    dateRetourPrevue = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'transactionEmprunt'

class Facture(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    montant_amende = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    path_facture_pdf =  models.CharField()
    class Meta:
        db_table = 'facture'