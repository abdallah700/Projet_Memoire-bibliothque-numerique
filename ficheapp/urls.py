from django.urls import path
from . import views

urlpatterns = [
    path('', views.fiche_list, name='fiche_list'),
    path('fiche/create/', views.fiche_create, name='fiche_create'),
    path('fiche/<int:fiche_id>/', views.fiche_detail, name='fiche_detail'),
    path('fiche/<int:fiche_id>/consultation/create/', views.consultation_create, name='consultation_create'),

    path('statistics/', views.statistics_view, name='statistics'),
    path('api/statistics/', views.get_statistics_data, name='get_statistics_data'),
    path('api/cons_statistics/', views.monthly_consultations_statistics, name='cons_statistics'),

    path('import_cote/', views.importExcel, name='import_cote'),
    path('import_discipline/', views.importDiscipl, name='import_discipline'),

]

