# rating/models.py
from django.db import models

class Rating(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='ratings')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='ratings')
    note = models.IntegerField()
    commentaire = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rating'