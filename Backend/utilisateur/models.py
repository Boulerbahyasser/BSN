# utilisateur/models.py
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class Utilisateur(AbstractUser,PermissionsMixin):
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = "Utilisateur"  # Rename the database table




class Demande(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='demandes')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='demandes')
    date_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demande'