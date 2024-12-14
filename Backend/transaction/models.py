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

    @staticmethod
    def get_attributes():
        return [field.name for field in Transaction._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur.id,
            'livre_id': self.livre.id,
            'type': self.type,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'montant': str(self.montant),
            'type_livre': self.type_livre
        }

    @classmethod
    def serialize_to_json(cls, queryset):
        return [transaction.to_dict() for transaction in queryset]


class TransactionEmprunt(Transaction):
    dateRetour = models.DateField(null=True, blank=True)
    dateRetourPrevue = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'transactionEmprunt'

    @staticmethod
    def get_attributes():
        return [field.name for field in TransactionEmprunt._meta.fields]

    def to_dict(self):
        # You can extend the base `to_dict` method if needed
        data = super().to_dict()
        data.update({
            'dateRetour': self.dateRetour.strftime('%Y-%m-%d') if self.dateRetour else None,
            'dateRetourPrevue': self.dateRetourPrevue.strftime('%Y-%m-%d') if self.dateRetourPrevue else None
        })
        return data

    @classmethod
    def serialize_to_json(cls, queryset):
        return [transaction.to_dict() for transaction in queryset]


class Facture(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    montant_amende = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    path_facture_pdf = models.CharField(max_length=255)

    class Meta:
        db_table = 'facture'

    @staticmethod
    def get_attributes():
        return [field.name for field in Facture._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction.id,
            'montant': str(self.montant),
            'montant_amende': str(self.montant_amende) if self.montant_amende else None,
            'date_creation': self.date_creation.strftime('%Y-%m-%d %H:%M:%S'),
            'path_facture_pdf': self.path_facture_pdf
        }

    @classmethod
    def serialize_to_json(cls, queryset):
        return [facture.to_dict() for facture in queryset]
