from django.db import models
from datetime import timedelta

class Fiche(models.Model):
    GENRE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin')
    ]

    nom_complet = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    annee_academique = models.CharField(max_length=11, blank=True, null=True)
    promotion_filiere = models.CharField(max_length=255, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True)  # Nouveau champ
    numero_fiche = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('numero_fiche', 'annee_academique', 'nom_complet')

class Consultation(models.Model):
    PHYSIQUE = 'P'
    NUMERIQUE = 'N'
    CONSULTATION_TYPE_CHOICES = [
        (PHYSIQUE, 'Physique'),
        (NUMERIQUE, 'Numérique'),
    ]

    fiche = models.ForeignKey(Fiche, related_name='consultations', on_delete=models.CASCADE, blank=True, null=True)
    type_consultation = models.CharField(max_length=1, choices=CONSULTATION_TYPE_CHOICES, blank=True, null=True)
    date = models.DateField()
    cote_livre = models.CharField(max_length=100, blank=True, null=True)
    no_inventaire_livre = models.CharField(max_length=100, blank=True, null=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    nombre_heures = models.DurationField(blank=True, null=True)
    observations = models.BooleanField(default=False)
    domaine_recherche = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.heure_debut and self.heure_fin:
            debut = timedelta(hours=self.heure_debut.hour, minutes=self.heure_debut.minute, seconds=self.heure_debut.second)
            fin = timedelta(hours=self.heure_fin.hour, minutes=self.heure_fin.minute, seconds=self.heure_fin.second)
            self.nombre_heures = fin - debut
        else:
            self.nombre_heures = None
        super().save(*args, **kwargs)
