from django.db import models


class Notification(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name="notifications")
    contenu = models.TextField()
    type = models.CharField(max_length=50)
    date_envoi = models.DateTimeField(auto_now_add=True)
    attachement = models.CharField(max_length=255, null=True, blank=True, default=None)  # Use None for default
    read_status = models.BooleanField(default=False)
    class Meta:
        db_table = 'notification'

    @staticmethod
    def get_attributes():
        return [field.name for field in Notification._meta.fields]

    def to_dict(self):
        return {
            'id': self.id,
            'utilisateur_id': self.utilisateur.id,
            'contenu': self.contenu,
            'type': self.type,
            'date_envoi': self.date_envoi.strftime('%Y-%m-%d %H:%M:%S'),
            'attachement': self.attachement,
        }

    @classmethod
    def serialize_to_json(cls, query):
        return [notification.to_dict() for notification in query]
