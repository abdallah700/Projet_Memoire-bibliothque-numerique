# fiches/forms.py
from django import forms
from .models import Visiteur, BibliothequePhysique, BibliothequeNumerique, CoteLivre, Discipline


# fiches/forms.py
from django import forms
from .models import Visiteur

class VisiteurForm(forms.ModelForm):
    class Meta:
        model = Visiteur
        fields = ['etudiant', 'biblio', 'autre', 'role']

class BibliothequePhysiqueForm(forms.ModelForm):
    class Meta:
        model = BibliothequePhysique

        fields = ['visiteur', 'coteLivre', 'numero_inventaire_livre', 'observation']
        
        widgets = {
            'date': forms.HiddenInput(),
        }
class BibliothequeNumeriqueForm(forms.ModelForm):
    class Meta:
        model = BibliothequeNumerique

        fields = ['visiteur', 'discipline']
        widgets = {
            'date': forms.HiddenInput(),
        }

class CoteLivreForm(forms.Form):
    class meta:
        model = CoteLivre
        fields = '__all__'

class DisciplineForm(forms.Form):
    class meta:
        model = Discipline
        fields = '__all__'