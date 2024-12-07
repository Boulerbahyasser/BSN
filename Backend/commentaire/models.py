# commentaire/models.py
from django.db import models

class Commentaire(models.Model):
    contenu = models.TextField()
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='commentaires')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='commentaires')
    note = models.IntegerField()

    class Meta:
        db_table = 'commentaire'