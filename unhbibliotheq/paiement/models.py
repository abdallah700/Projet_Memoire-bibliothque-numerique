from django.db import models
from .models import Utilisateur, Bibliothecaire
# Create your models here.


class Annee_academique(models.Model):
    nomAnnee = models.DateField(auto_now = True)
    is_actif = models.BooleanField('is actif', default=False)

class Paiement(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    estAJour = models.BooleanField('est à jour',default=False)
    montantTotalAPayer = models.FloatField()
    statut = models.BooleanField('statut', default=False)

class Libraifi(models.Model):
    annee_academique = models.ForeignKey(Annee_academique, related_name='annee academique', on_delete=models.CASCADE)
    paiement = models.ForeignKey(Paiement, related_name='paiement', on_delete=models.CASCADE)
    sommeAPayer = models.FloatField()
    statut = models.BooleanField('statut', default=False)


class Message(models.Model):
    titremsg = models.CharField(max_length = 200)
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    bibliothecaire = models.ForeignKey(Bibliothecaire, related_name='bibliothecaire', on_delete=models.CASCADE)

