
from django.urls import path
from .views import detail_fiche, recherche_visiteur, ajouter_informations_quotidiennes, bibliotheque_numerique, importExcel, importDiscipl, statistiques_etudiants

app_name = 'fiches'

urlpatterns = [
    path('', detail_fiche, name='detail-fiche'),
    path('recherche-visiteur/', recherche_visiteur, name='recherche-visiteur'),
    path('ajouter-informations-quotidiennes/<int:visiteur_id>/', ajouter_informations_quotidiennes, name='ajouter-informations-quotidiennes'),
    path('bibliotheque-numerique/<int:visiteur_id>/', bibliotheque_numerique, name='bibliotheque-numerique'),
    path('import-excel/', importExcel, name='import-excel'),
    path('import-discipline/', importDiscipl, name='import-discipline'),

    path('fiches/statistiques_etudiants/<int:annee>/<int:mois>/', statistiques_etudiants, name='statistiques_etudiants'),
]
