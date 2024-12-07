from django.db import models


class Notification(models.Model):
    utilisateur = models.ForeignKey('utilisateur.Utilisateur', on_delete=models.CASCADE, related_name="notifications")
    contenu = models.TextField()
    type = models.CharField(max_length=50)
    date_envoi = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'notification'