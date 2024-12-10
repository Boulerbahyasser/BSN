# utilisateur/models.py
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
class Utilisateur(AbstractUser, PermissionsMixin):
    description = models.TextField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "Utilisateur"  # Rename the database table

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_staff': self.is_staff,
            'is_superuser': self.is_superuser,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M:%S') if self.last_login else None,  # Added field from AbstractUser
            'date_joined': self.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description,
            'image': self.image,
            'telephone': self.telephone,
            'adresse': self.adresse,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [user.to_dict() for user in query]




class Demande(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='demandes')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='demandes')
    date_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'demande'

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur.id,
            'livre_id': self.livre.id,
            'date_demande': self.date_demande.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [demande.to_dict() for demande in query]