# livre/models.py
from django.db import models

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    couverture_path = models.CharField(max_length=255, null=True, blank=True)  # Store path as a string
    auteur = models.CharField(max_length=100)
    est_disponible = models.BooleanField(default=True)
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='livres')
    class Meta:
        db_table = 'livre'

    @staticmethod
    def get_attributes():
        return [field.name for field in Livre._meta.fields]
    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'couverture_path': self.couverture_path,
            'auteur': self.auteur,
            'est_disponible': self.est_disponible,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [livre.to_dict() for livre in query]


class LivrePhysique(Livre):  # Inherits from Livre
    dimensions = models.CharField(max_length=100)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    stock_vente = models.IntegerField(default=0)
    stock_emprunt = models.IntegerField(default=0)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    prix_emprunt_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    taux_amende = models.DecimalField(max_digits=5, decimal_places=2)
    vendus = models.IntegerField(default=0)
    empruntes = models.IntegerField(default=0)

    class Meta:
        db_table = 'livrePhysique'

    @staticmethod
    def get_attributes():
        return [field.name for field in LivrePhysique._meta.fields]


    def to_dict(self):
        base_dict = super().to_dict()  # Get the dictionary from the parent (Livre)
        base_dict.update({
            'dimensions': self.dimensions,
            'poids': str(self.poids),
            'stock_vente': self.stock_vente,
            'stock_emprunt': self.stock_emprunt,
            'prix_vente': str(self.prix_vente),
            'prix_emprunt_par_jour': str(self.prix_emprunt_par_jour),
            'taux_amende': str(self.taux_amende),
            'vendus': self.vendus,
            'empruntes': self.empruntes,
        })
        return base_dict

    @classmethod
    def serialize_to_json(cls, query):
        return [livre.to_dict() for livre in query]



class LivreNumerique(Livre):
    path_livre_pdf = models.CharField(max_length=255)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'livreNumerique'

    @staticmethod
    def get_attributes():
        return [field.name for field in LivreNumerique._meta.fields]

    def to_dict(self):
        base_dict = super().to_dict()  # Get the dictionary from the parent (Livre)
        base_dict.update({
            'path_livre_pdf': self.path_livre_pdf,
            'prix_vente': str(self.prix_vente),
        })
        return base_dict

    @classmethod
    def serialize_to_json(cls, query):
        return [livre.to_dict() for livre in query]




class Category(models.Model):
    nom = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'

    @staticmethod
    def get_attributes():
        return [field.name for field in Category._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [category.to_dict() for category in query]



class LivreCategory(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'livreCategory'

    @staticmethod
    def get_attributes():
        return [field.name for field in LivreCategory._meta.fields]


    def to_dict(self):
        return {
            'id': self.id,
            'livre_id': self.livre.id,
            'category_id': self.category.id,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [livre_category.to_dict() for livre_category in query]
