# livre/models.py
from django.db import models


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    couverture_path = models.CharField(max_length=255, null=True, blank=True)  # Store path as a string
    auteur = models.CharField(max_length=100)
    est_disponible = models.BooleanField(default=True)
    class Meta:
        db_table = 'livre'


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


class LivreNumerique(Livre):
    path_livre_pdf = models.CharField()
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'livreNumerique'




class Category(models.Model):
    nom = models.CharField(max_length=255)
    class Meta:
        db_table = 'category'



class LivreCategory(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'livreCategory'