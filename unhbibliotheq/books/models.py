from django.db import models
from .models import Categorie_books, Utilisateur

# Create your models here.
class Categorie_books(models.Model):
    nomCategorie = models.ForeignKey(Categorie_books, related_name='categorie_books', on_delete=models.CASCADE)
    domaine_books = models.CharField(max_length=200)

class Books(models.Model):
    categorie_books = models.ForeignKey(Categorie_books, related_name='categorie_books', on_delete=models.CASCADE)
    titre = models.CharField(max_length = 200)
    auteur = models.CharField(max_langth = 200)
    numInventaire = models.CharField(max_length = 200)
    isbn = models.CharField(max_length=200)
    nombrePage = models.IntegerField()
    nombreExemplaire = models.IntegerField()
    maisonEdition = models.CharField(max_length = 200)
    isbn = models.CharField(max_length=200)
    catalogue = models.CharField(max_length=200)
    is_Consulter = models.BooleanField('is consulter', default=False)
    is_Reserver = models.BooleanField('is Reserver', default=False)
    is_Emprunter = models.BooleanField('is emprunter', default=False)


class Type_consulter(models.Model):
    on_line = models.BooleanField('type consulter', default=False)
    physically = models.BooleanField('physically', default=False)

class Consulter(models.Model):
    books = models.ForeignKey(Books, related_name='books', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    type_consulter = models.ForeignKey(Type_consulter, related_name='type consulter', on_delete=models.CASCADE)
    date = models.DateField(auto_now = True)
    heurArrivee = models.DateTimeField(auto_now = True)
    heureRetour = models.DateTimeField(auto_now = True)
    statut = models.BooleanField('statut', default=False)

class Reserver(models.Model):
    books = models.ForeignKey(Books, related_name='books', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    dateHReserve = models.DateTimeField(auto_now = True)
    dateHRetour = models.DateTimeField(auto_now = True)
    penalite = models.FloatField()
    statut = models.BooleanField('statut', default=False)

class Emprunter(models.Model):
    books = models.ForeignKey(Books, related_name='books', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, related_name='utilisateur', on_delete=models.CASCADE)
    dateEmprunt = models.DateField(auto_now = True)
    dateRetour = models.DateField(auto_now = True)
    penalite = models.FloatField()
    statut = models.BooleanField('statut', default=False)
