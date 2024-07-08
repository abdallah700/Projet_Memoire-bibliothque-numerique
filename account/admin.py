from django.contrib import admin
from .models import CategorieScientifique, EtudiantInterne, Promotion, Faculte, Filiere, Bibliothecaire, AutrePersonneScientifique

# Register your models here.


admin.site.register(CategorieScientifique)
admin.site.register(EtudiantInterne)
admin.site.register(Promotion)
admin.site.register(Faculte)
admin.site.register(Filiere)
admin.site.register(Bibliothecaire)
admin.site.register(AutrePersonneScientifique)

