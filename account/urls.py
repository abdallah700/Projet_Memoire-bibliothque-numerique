from django.urls import path
from .views import signin_view, signupEtInterne_view,signupAutrSc_view, signupBiblioth_view, Filiere_view, Faculte_view, Promotion_view, CategorieScientifique_view, Annee_academique_view

urlpatterns = [
    # ... vos autres URL ...
    path('', signin_view, name='con'),
    path('signupEtInt/', signupEtInterne_view, name='signupEtInt'),
    path('signupAS/', signupAutrSc_view, name='signupAS'),
    path('signupBib/', signupBiblioth_view, name='signupBib'),

    path('Filiere/', Filiere_view, name='Filiere'),
    path('Faculte/', Faculte_view, name='Faculte'),
    path('Promotion/', Promotion_view, name='Promotion'),
    path('CategorSc_form/', CategorieScientifique_view, name='CategorSc_form'),
    path('Annee_academique/', Annee_academique_view, name='Annee_academique'),
]

