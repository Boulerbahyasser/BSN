# commentaire/models.py
from django.db import models


class Commentaire(models.Model):
    contenu = models.TextField()
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='commentaires')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='commentaires')
    note = models.IntegerField()

    class Meta:
        db_table = 'commentaire'

    @staticmethod
    def get_attributes():
        return [field.name for field in Commentaire._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'contenu': self.contenu,
            'utilisateur_id': self.utilisateur.id,
            'livre_id': self.livre.id,
            'note': self.note,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [commentaire.to_dict() for commentaire in query]
