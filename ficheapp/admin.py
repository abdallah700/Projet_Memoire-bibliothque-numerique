from django.contrib import admin

# Register your models here.
from .models import Fiche, Consultation, CoteLivre, Discipline

# Register your models here.


admin.site.register(Fiche)
admin.site.register(Consultation)
admin.site.register(CoteLivre)
admin.site.register(Discipline)