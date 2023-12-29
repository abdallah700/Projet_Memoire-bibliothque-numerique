from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_bibliothecaire = models.BooleanField('Is bibliothecaire', default=False)
    is_etudiantInterne = models.BooleanField('Is etudiantInterne', default=False)
    is_personneInterne = models.BooleanField('Is personneInterne', default=False)
    is_personneExterne = models.BooleanField('Is personneExterne', default=False)
    
