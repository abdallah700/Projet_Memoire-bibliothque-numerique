from django.shortcuts import render, redirect
from .forms import BibliothequePhysiqueForm, BibliothequeNumeriqueForm
from django.shortcuts import get_object_or_404
from .models import Visiteur, BibliothequePhysique, BibliothequeNumerique, CoteLivre, Discipline
from django.http import Http404, HttpResponse
from account.models import *
from tablib import Dataset
from .resources import CoteLivreResource, DisciplineResource
from django.shortcuts import render
from .models import Visiteur, EtudiantInterne
from django.shortcuts import render, HttpResponse
from django.db.models import Count, Case, When, IntegerField



def detail_fiche(request):
    numero_fiche = request.GET.get('numero_fiche')
    nom_complet = request.GET.get('nom_complet')
    instance = None
    histo = None
    photo_profil = None
    histonumerique = None
    type_utl = None

    if numero_fiche:
        visiteur = None
        if EtudiantInterne.objects.filter(numero_fiche=numero_fiche).exists():
            visiteur = Visiteur.objects.get(etudiant=EtudiantInterne.objects.get(numero_fiche=numero_fiche))
            type_utl = visiteur.etudiant
            photo_profil = type_utl.photo_profil
        elif AutrePersonneScientifique.objects.filter(numero_fiche=numero_fiche).exists():
            visiteur = Visiteur.objects.get(autre=AutrePersonneScientifique.objects.get(numero_fiche=numero_fiche))
            type_utl = visiteur.autre
            photo_profil = type_utl.photo_profil
        instance = visiteur
        histo = BibliothequePhysique.objects.filter(visiteur=instance)
        histonumerique = BibliothequeNumerique.objects.filter(visiteur=instance)
    elif nom_complet:
        visiteur = None
        if EtudiantInterne.objects.filter(nom_complet__icontains=nom_complet).exists():
            etudiant = EtudiantInterne.objects.filter(nom_complet__icontains=nom_complet).first()
            numero_fiche = etudiant.numero_fiche  # Pre-fill numero_fiche
            visiteur = Visiteur.objects.get(etudiant=etudiant)
            type_utl = visiteur.etudiant
            photo_profil = type_utl.photo_profil
        elif AutrePersonneScientifique.objects.filter(nom_complet__icontains=nom_complet).exists():
            autre = AutrePersonneScientifique.objects.filter(nom_complet__icontains=nom_complet).first()
            numero_fiche = autre.numero_fiche  # Pre-fill numero_fiche
            visiteur = Visiteur.objects.get(autre=autre)
            type_utl = visiteur.autre
            photo_profil = type_utl.photo_profil
        instance = visiteur
        histo = BibliothequePhysique.objects.filter(visiteur=instance)
        histonumerique = BibliothequeNumerique.objects.filter(visiteur=instance)

    return render(request, 'fiches/detail_fiche.html', {
        'instance': instance,
        'histo': histo,
        'histonumerique': histonumerique,
        'type_utl': type_utl,
        'photo_profil': photo_profil,
        'numero_fiche': numero_fiche,  # Pass numero_fiche to the template
        'nom_complet': nom_complet  # Pass nom_complet to the template
    })

def recherche_visiteur(request):
    visiteur = None
    error_message = None
    photo_profil = None
    if request.method == 'GET':
        return render(request, 'fiches/recherche_visiteur.html')
    elif request.method == 'POST':
        numero_fiche = request.POST.get('numero_fiche', None)

        if numero_fiche:
            if EtudiantInterne.objects.filter(numero_fiche=numero_fiche).exists():
                visiteur = Visiteur.objects.get(etudiant__numero_fiche=numero_fiche)
                type_utl = visiteur.etudiant
                photo_profil = type_utl.photo_profil
                return redirect('fiches:ajouter-informations-quotidiennes', visiteur_id=visiteur.id)
            elif AutrePersonneScientifique.objects.filter(numero_fiche=numero_fiche).exists():
                visiteur = Visiteur.objects.get(autre__numero_fiche=numero_fiche)
                type_utl = visiteur.autre
                photo_profil = type_utl.photo_profil
                return redirect('fiches:ajouter-informations-quotidiennes', visiteur_id=visiteur.id)
            else:
                error_message = "Aucun visiteur trouvé avec ce numéro de fiche."

        return render(request, 'fiches/recherche_visiteur.html', {'error_message': error_message, 'photo_profil': photo_profil })

def ajouter_informations_quotidiennes(request, visiteur_id):
    visiteur = Visiteur.objects.get(pk=visiteur_id)
    cotes_livres = CoteLivre.objects.all()
    disciplines = Discipline.objects.all()
    type_utl = None
    photo_profil = None
    if EtudiantInterne.objects.filter(visiteur=visiteur).exists():
        visiteur = Visiteur.objects.get(etudiant__visiteur=visiteur)
        type_utl = visiteur.etudiant
        photo_profil = type_utl.photo_profil
    elif AutrePersonneScientifique.objects.filter(visiteur=visiteur).exists():
        visiteur =  Visiteur.objects.get(autre__visiteur=visiteur)
        type_utl = visiteur.autre
        photo_profil = type_utl.photo_profil
    if request.method == 'POST':
        date = request.POST.get('date', None)
        numero_inventaire = request.POST.get('numero_inventaire', None)
        cote_livre_id = request.POST.get('cote_livre')
        observation = request.POST.get('observation', False)
        cote = CoteLivre.objects.get(id=cote_livre_id)
        bibliotheque_physique = BibliothequePhysique.objects.create(
            visiteur=visiteur,
            date=date,
            numero_inventaire_livre=numero_inventaire,
            coteLivre = cote,
            observation=True
        )

        return redirect('fiches:detail-fiche')
    else:
        return render(request, 'fiches/ajouter_informations_quotidiennes.html',
                      {'visiteur': visiteur,
                                'type': type_utl,
                                'cotes_livres': cotes_livres,
                                'disciplines': disciplines,
                                'photo_profil': photo_profil })

def bibliotheque_numerique(request, visiteur_id):
    visiteur = Visiteur.objects.get(pk=visiteur_id)
    disciplines = Discipline.objects.all()
    type_utl = None

    if EtudiantInterne.objects.filter(visiteur=visiteur).exists():
        visiteur = Visiteur.objects.get(etudiant__visiteur=visiteur)
        type_utl = visiteur.etudiant
        photo_profil = type_utl.photo_profil
    elif AutrePersonneScientifique.objects.filter(visiteur=visiteur).exists():
        visiteur = Visiteur.objects.get(autre__visiteur=visiteur)
        type_utl = visiteur.autre
        photo_profil = type_utl.photo_profil
    if request.method == 'POST':
        date = request.POST.get('date', None)
        domaine_recherche_id = request.POST.get('discipline')
        domaine = Discipline.objects.get(id=domaine_recherche_id)
        bibliotheque_numerique = BibliothequeNumerique.objects.create(
            visiteur=visiteur,
            date=date,
            discipline=domaine

        )

        return redirect('fiches:detail-fiche')
    else:
        return render(request, 'fiches/bibliotheque_numerique.html',
                      {'visiteur': visiteur,
                       'type': type_utl,
                       'disciplines': disciplines,
                       'photo_profil': photo_profil })

def importExcel(request):
    if request.method == 'POST':
        CoteLivre_Resource = CoteLivreResource()
        dataset = Dataset()
        new_coteLivre = request.FILES.get('my_file')  # Utilisez get() au lieu de l'indexation []
        if new_coteLivre:
            imported_data = dataset.load(new_coteLivre.read(), format='xlsx')
            for data in imported_data:
                value = CoteLivre(
                    data[0],
                    data[1]
                )
                value.save()
    return render(request, 'fiches/impExp.html')

def importDiscipl(request):
    if request.method == 'POST':
        Discipline_Resource = DisciplineResource()
        dataset = Dataset()
        new_discipline = request.FILES.get('my_file')  # Utilisez get() au lieu de l'indexation []
        if new_discipline:
            imported_data = dataset.load(new_discipline.read(), format='xlsx')
            for data in imported_data:
                value = Discipline(
                    data[0],
                    data[1]
                )
                value.save()
    return render(request, 'fiches/importDiscipline.html')


def ajouter_fac(facs, fac):
    if fac not in facs:
        facs[fac] = {}

def ajouter_promo(facs, fac, promo, m, f):
    if fac in facs:
        facs[fac][promo] = [m, f]

def statistiques_etudiants(request, annee, mois):
    statistiques_physique = None
    statistiques_numerique = None
    type_utl = None
    date_recherche = request.GET.get('date')
    facultes = Faculte.objects.all()
    nombre_autre = AutrePersonneScientifique.objects.all()

    stat_physique = {}
    for i in facultes:
        ajouter_fac(stat_physique, i.nom_faculte)
        for j in Promotion.objects.filter(faculte=i):
            ajouter_promo(stat_physique, i.nom_faculte, j.nom_promotion, 0, 0)

    visites = BibliothequePhysique.objects.filter(date__year=annee, date__month=mois)
    nbr_m = 0
    nbr_f = 0
    promotions = Promotion.objects.all()
    count = 0
    for i in visites:
        if i.visiteur.etudiant is not None:
            if i.visiteur.etudiant.genre == 'M':
                stat_physique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][0] = stat_physique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][0]+1
            else:
                stat_physique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][1] = stat_physique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][1]+1



    stat_numerique = {}
    for i in facultes:
        ajouter_fac(stat_numerique, i.nom_faculte)
        for j in Promotion.objects.filter(faculte=i):
            ajouter_promo(stat_numerique, i.nom_faculte, j.nom_promotion, 0, 0)

    visites = BibliothequeNumerique.objects.filter(date__year=annee, date__month=mois)
    nbr_m = 0
    nbr_f = 0
    promotions = Promotion.objects.all()
    count = 0
    for i in visites:
        if i.visiteur.etudiant is not None:
            if i.visiteur.etudiant.genre == 'M':
                stat_numerique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][0] = stat_numerique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][0]+1
            else:
                stat_numerique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][1] = stat_numerique[i.visiteur.etudiant.faculte.nom_faculte][i.visiteur.etudiant.promotion.nom_promotion][1]+1
    # total general
    total_general = {'physique': {'homme': 0, 'femme': 0}, 'numerique': {'homme': 0, 'femme': 0}}
    total_par_faculte = {}

    # Calcul des statistiques pour les personnes externes en bibliothèque physique
    stat_physique_externe = {'homme': 0, 'femme': 0}
    visites_physique = BibliothequePhysique.objects.filter(date__year=annee, date__month=mois)
    for visite in visites_physique:
        if visite.visiteur.autre is not None:
            if visite.visiteur.autre.genre == 'M':
                stat_physique_externe['homme'] += 1
            else:
                stat_physique_externe['femme'] += 1

    # Ajout des statistiques externes au total général pour la bibliothèque physique
    total_general['physique']['homme'] += stat_physique_externe['homme']
    total_general['physique']['femme'] += stat_physique_externe['femme']

    # Code existant...

    # Calcul des statistiques pour les personnes externes en bibliothèque numérique
    stat_numerique_externe = {'homme': 0, 'femme': 0}
    visites_numerique = BibliothequeNumerique.objects.filter(date__year=annee, date__month=mois)
    for visite in visites_numerique:
        if visite.visiteur.autre is not None:
            if visite.visiteur.autre.genre == 'M':
                stat_numerique_externe['homme'] += 1
            else:
                stat_numerique_externe['femme'] += 1

    # Ajout des statistiques externes au total général pour la bibliothèque numérique
    total_general['numerique']['homme'] += stat_numerique_externe['homme']
    total_general['numerique']['femme'] += stat_numerique_externe['femme']

    # Calcul des totaux par faculté
    for faculte, promotions in stat_physique.items():
        total_par_faculte[faculte] = {'physique': {'homme': 0, 'femme': 0}, 'numerique': {'homme': 0, 'femme': 0}}
        for promotion, stats in promotions.items():
            total_par_faculte[faculte]['physique']['homme'] += stats[0]
            total_par_faculte[faculte]['physique']['femme'] += stats[1]
        # Ajouter les statistiques externes par faculté pour la bibliothèque physique
        total_par_faculte[faculte]['physique']['homme'] += stat_physique_externe['homme']
        total_par_faculte[faculte]['physique']['femme'] += stat_physique_externe['femme']

    for faculte, promotions in stat_numerique.items():
        for promotion, stats in promotions.items():
            total_par_faculte[faculte]['numerique']['homme'] += stats[0]
            total_par_faculte[faculte]['numerique']['femme'] += stats[1]
        # Ajouter les statistiques externes par faculté pour la bibliothèque numérique
        total_par_faculte[faculte]['numerique']['homme'] += stat_numerique_externe['homme']
        total_par_faculte[faculte]['numerique']['femme'] += stat_numerique_externe['femme']


    print(total_general)

    return render(request, 'fiches/statistiques.html', {
        'statistiques_physique': stat_physique,
        'statistiques_numerique': stat_numerique,
        'type': type_utl,
        'stat_physique_externe': stat_physique_externe,
        'stat_numerique_externe':stat_numerique_externe,
        'total_par_faculte': total_par_faculte,
        'total_general': total_general
    })