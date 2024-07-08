from django.contrib import admin

# Register your models here.
from .models import Fiche, Consultation

# Register your models here.


admin.site.register(Fiche)
admin.site.register(Consultation)