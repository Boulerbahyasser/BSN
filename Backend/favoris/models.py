# favoris/models.py
from django.db import models

class Favoris(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='favoris')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='favoris')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favoris'

    @staticmethod
    def get_attributes():
        return [field.name for field in Favoris._meta.fields]
    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur.id,
            'livre_id': self.livre.id,
            'date_ajout': self.date_ajout.strftime('%Y-%m-%d %H:%M:%S'),
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [favoris.to_dict() for favoris in query]
