from django.db import models
# Create your models here.
from django.urls import reverse
from account.models import *
roles = (
    ('Etudiant', 'Etudiant'),
    ('Bibliothecaire', 'Bibliothecaire'),
    ('Autre', 'Autre'),
)

class Visiteur(models.Model):
    etudiant = models.ForeignKey(EtudiantInterne, on_delete=models.CASCADE, null=True)
    biblio = models.ForeignKey(Bibliothecaire, on_delete=models.CASCADE, null=True)
    autre = models.ForeignKey(AutrePersonneScientifique, on_delete=models.CASCADE, null=True)
    role = models.CharField(choices=roles, max_length=255, null=True)

    def __str__(self):
        name = ''
        if self.etudiant is not None:
            name = self.etudiant.nom_complet
        elif self.autre is not None:
            name = self.autre.nom_complet
        else:
            name = self.biblio.nom_complet
        return name
    @property
    def get_role(self):
        role = None
        if self.etudiant is None and self.biblio is None:
            role = roles[2][1]
        elif self.etudiant is None and self.autre is None:
            role = roles[1][1]
        elif self.biblio is None and self.autre is None:
            role = roles[1][1]
        return role
    
class CoteLivre(models.Model):
    cote_livre = models.CharField(max_length=250)
    nb_selections = models.IntegerField(default=0)
    def __str__(self):
        return str(self.cote_livre)

class Discipline(models.Model):
    domaine_recherche = models.CharField(max_length=250)
    nb_selections = models.IntegerField(default=0)  # Champ pour enregistrer le nombre de sélections
    def __str__(self):
        return self.domaine_recherche

class BibliothequePhysique(models.Model):
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    coteLivre = models.ForeignKey(CoteLivre, related_name='coteLivre', on_delete=models.CASCADE)
    numero_inventaire_livre = models.CharField(max_length=50)
    observation = models.BooleanField()
    def __str__(self): 
        return str(self.date)

class BibliothequeNumerique(models.Model):
    visiteur = models.ForeignKey(Visiteur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    discipline = models.ForeignKey(Discipline, related_name='discipline', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.date)

