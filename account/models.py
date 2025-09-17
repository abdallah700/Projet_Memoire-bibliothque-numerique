from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from bookapp import settings

class CategorieScientifique(models.Model):
    categorie_scientifique = models.CharField(max_length=255)
    
    def __str__(self):
        return self.categorie_scientifique

class Bibliothecaire(models.Model):
    nom_complet = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    numero_telephone = models.CharField(max_length=15)
    email = models.EmailField()
    photo_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    date = models.DateTimeField(auto_now = True)
    specialite = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nom_complet + " (" + self.specialite + ")"

    def get_photo_profil_url(self):
        if self.photo_profil and self.photo_profil.name:
            return self.photo_profil.url
        return None

class Faculte(models.Model):
    nom_faculte = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_faculte

class Filiere(models.Model):
    faculte = models.ForeignKey(Faculte, null=True, on_delete=models.CASCADE)
    nom_filiere = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_filiere

class Promotion(models.Model):
    faculte = models.ForeignKey(Faculte, null=True, on_delete=models.CASCADE)
    nom_promotion = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_promotion

class EtudiantInterne(models.Model):
    numero_fiche = models.IntegerField()
    nom_complet = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    numero_telephone = models.CharField(max_length=15)
    email = models.EmailField()
    photo_profil = models.ImageField(upload_to='profil_photos/', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    promotion = models.ForeignKey(Promotion, related_name='etudiants', on_delete=models.CASCADE)
    faculte = models.ForeignKey(Faculte, related_name='etudiants', on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, related_name='etudiants', on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_complet + " (" + "EtudiantInterne" + ")"

class AutrePersonneScientifique(models.Model):
    numero_fiche = models.IntegerField()
    nom_complet = models.CharField(max_length=255)
    genre = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True)
    numero_telephone = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    photo_profil = models.ImageField(upload_to='profil_photos/', null=True, blank=True)
    date = models.DateTimeField(auto_now = True)
    titre_academique = models.CharField(max_length=255, null=True)
    nom_etablissement = models.CharField(max_length=255, null=True)
    adresse_etablissement = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nom_complet + " (" + "AutrePersonneScientifique" + ")"

class Annee_academique(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    annee_academique = models.CharField(max_length=20)

    def __str__(self):
        return self.annee_academique

@receiver(post_save, sender=EtudiantInterne)
def create_etudiant(sender, instance, created, **kwargs):
    if created:
        from fiches.models import Visiteur
        Visiteur.objects.create(etudiant=instance, role='Etudiant')

@receiver(post_save, sender=AutrePersonneScientifique)
def create_visiteur(sender, instance, created, **kwargs):
    if created:
        from fiches.models import Visiteur
        Visiteur.objects.create(autre=instance, role='Autre')
