from django.contrib import admin

# Register your models here.
# fiches/admin.py

from .models import Visiteur, BibliothequePhysique, BibliothequeNumerique, CoteLivre

admin.site.register(Visiteur)
admin.site.register(BibliothequePhysique)
admin.site.register(BibliothequeNumerique)
admin.site.register(CoteLivre)
