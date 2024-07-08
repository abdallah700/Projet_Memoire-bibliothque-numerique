from django.urls import path
from . import views

urlpatterns = [
    path('', views.fiche_list, name='fiche_list'),
    path('fiche/create/', views.fiche_create, name='fiche_create'),
    path('fiche/<int:fiche_id>/', views.fiche_detail, name='fiche_detail'),
    path('fiche/<int:fiche_id>/consultation/create/', views.consultation_create, name='consultation_create'),
]

