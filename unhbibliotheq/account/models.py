from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Utilisateur(models.Model):
    nom = models.CharField(max_length = 200)
    prenom = models.CharField(max_langth = 200)
    password = models.CharField(max_length = 8)
    email = models.CharField(max_length = 200)
    date_created = models.DateField(auto_now = True)
    date_last_connection = models.DateField(auto_now = True)
    superuser = models.BooleanField('Is superuser', default=False)
    is_bibliothecaire = models.BooleanField('Is bibliothecaire', default=False)
    is_etudiantInterne = models.BooleanField('Is etudiantInterne', default=False)
    is_personneInterne = models.BooleanField('Is personneInterne', default=False)
    is_personneExterne = models.BooleanField('Is personneExterne', default=False)


class Bibliothecaire(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    specialite = models.CharField(max_length = 200)

class EtudiantInterne(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    promotion = models.CharField(max_length = 200)
    departement = models.CharField(max_langth = 200)
    filiere = models.CharField(max_length = 200)


class Categorie_personne_interne(models.Model):
    nomCategorie = models.CharField(max_length = 200)


class PersonneInterne(models.Model):
    categorie_personne_interne = models.ForeignKey(Categorie_personne_interne, related_name='Categorie_personne_interne', on_delete=models.CASCADE)
    point_recherche = models.CharField(max_length = 200)


class Categorie_personne_Externe(models.Model):
    nomCategorie = models.CharField(max_length = 200)


class PersonneExterne(models.Model):
    categorie_personne_interne = models.ForeignKey(Categorie_personne_Externe, related_name='Categorie_personne_Externe', on_delete=models.CASCADE)
    adresse = models.CharField(max_langth = 200)
    nom = models.CharField(max_length = 200)
    point_recherche = models.CharField(max_langth = 200)
