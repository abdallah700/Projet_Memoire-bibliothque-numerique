from import_export import resources
from .models import CoteLivre, Discipline

class CoteLivreResource(resources.ModelResource):
    class meta:
        model = CoteLivre

class DisciplineResource(resources.ModelResource):
    class meta:
        model = Discipline