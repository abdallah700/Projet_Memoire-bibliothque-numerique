from django import forms
from .models import Fiche, Consultation, CoteLivre, Discipline

class FicheForm(forms.ModelForm):
    class Meta:
        model = Fiche
        fields = ['nom_complet', 'genre', 'telephone', 'annee_academique', 'promotion_filiere', 'photo_profil', 'numero_fiche']
        widgets = {
            'genre': forms.Select(choices=Fiche.GENRE_CHOICES),
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'type_consultation', 'date', 'cote_livre', 'no_inventaire_livre',
            'heure_debut', 'heure_fin', 'nombre_heures', 'observations', 'domaine_recherche'
        ]
        widgets = {
            'type_consultation': forms.Select(choices=Consultation.CONSULTATION_TYPE_CHOICES),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'nombre_heures': forms.TimeInput(attrs={'type': 'time'}),
            'observations': forms.CheckboxInput(),
            'domaine_recherche': forms.Select(),
            'cote_livre': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super(ConsultationForm, self).__init__(*args, **kwargs)
        self.fields['cote_livre'].queryset = CoteLivre.objects.all()
        self.fields['domaine_recherche'].queryset = Discipline.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        heure_debut = cleaned_data.get('heure_debut')
        heure_fin = cleaned_data.get('heure_fin')

        if heure_debut and heure_fin and heure_debut >= heure_fin:
            raise forms.ValidationError("L'heure de début doit être avant l'heure de fin.")

        return cleaned_data

    class CoteLivreForm(forms.Form):
        class meta:
            model = CoteLivre
            fields = '__all__'

    class DisciplineForm(forms.Form):
        class meta:
            model = Discipline
            fields = '__all__'