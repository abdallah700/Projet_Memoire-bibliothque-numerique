# account/forms.py

from django import forms
from .models import Bibliothecaire, EtudiantInterne,  AutrePersonneScientifique, Filiere, Faculte, Promotion, CategorieScientifique,Annee_academique

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class BibliothecaireForm(forms.ModelForm):
    class Meta:
        model = Bibliothecaire

        fields = ['nom_complet', 'email', 'photo_profil', 'genre', 'numero_telephone','specialite']
        widgets = {
            'date': forms.HiddenInput(),
        }
class EtudiantInterneForm(forms.ModelForm):
    class Meta:
        model = EtudiantInterne

        fields = ['numero_fiche', 'nom_complet', 'email', 'photo_profil', 'genre', 'numero_telephone','promotion', 'faculte', 'filiere']
        widgets = {
            'date': forms.HiddenInput(),
        }


class AutrePersonneScientifiqueForm(forms.ModelForm):
    class Meta:
        model = AutrePersonneScientifique

        fields = ['numero_fiche', 'nom_complet', 'email', 'photo_profil', 'genre', 'numero_telephone','titre_academique', 'nom_etablissement', 'adresse_etablissement']
        widgets = {
            'date': forms.HiddenInput(),
        }

class FiliereForm(forms.ModelForm):
    class Meta:
        model = Filiere

        fields = ['nom_filiere',]
        widgets = {
            'date': forms.HiddenInput(),
        }

class FaculteForm(forms.ModelForm):
    class Meta:
        model = Faculte

        fields = ['nom_faculte']
        widgets = {
            'date': forms.HiddenInput(),
        }

class PromotionForm(forms.ModelForm):
        class Meta:
            model = Promotion

            fields = ['nom_promotion']
            widgets = {
                'date': forms.HiddenInput(),
            }

class CategorieScientifiqueForm(forms.ModelForm):
        class Meta:
            model = CategorieScientifique

            fields = ['categorie_scientifique']
            widgets = {
                'date': forms.HiddenInput(),
            }

class Annee_academiqueForm(forms.ModelForm):
        class Meta:
            model = Annee_academique
            fields = ['annee_academique']
            widgets = {
                'date': forms.HiddenInput(),
            }