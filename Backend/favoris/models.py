# favoris/models.py
from django.db import models

class Favoris(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='favoris')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='favoris')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favoris'