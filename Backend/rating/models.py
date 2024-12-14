from django.db import models


class Rating(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name='ratings')
    livre = models.ForeignKey('livre.Livre', on_delete=models.CASCADE, related_name='ratings')
    note = models.IntegerField()
    commentaire = models.TextField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rating'

    @staticmethod
    def get_attributes():
        return [field.name for field in Rating._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur.id,
            'livre_id': self.livre.id,
            'note': self.note,
            'commentaire': self.commentaire,
            'date_creation': self.date_creation.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [rating.to_dict() for rating in query]
