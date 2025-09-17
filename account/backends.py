# account/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from .models import Bibliothecaire

class BibliothecaireBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            bibliothecaire = Bibliothecaire.objects.get(email=email)
        except Bibliothecaire.DoesNotExist:
            return None

        if check_password(password, bibliothecaire.password):
            return bibliothecaire
        return None
