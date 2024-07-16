
from django.http import JsonResponse
from django.db.models import Count
from tablib import Dataset

from fiches.resources import CoteLivreResource, DisciplineResource
from .models import Fiche
from django.db.models.functions import TruncMonth
from collections import defaultdict
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
import openpyxl
from .models import CoteLivre, Discipline, Consultation
from .forms import FicheForm, ConsultationForm
from django.shortcuts import render, get_object_or_404
import calendar
import logging

logger = logging.getLogger(__name__)

def fiche_list(request):
    fiches = Fiche.objects.all()
    return render(request, 'ficheapp/fiche_list.html', {'fiches': fiches})





def fiche_detail(request, fiche_id):
    fiche = Fiche.objects.get(id=fiche_id)
    consultations = fiche.consultations.all()

    # Générer des labels pour tous les mois
    labels = [calendar.month_abbr[i] for i in range(1, 13)]

    # Préparer les données pour chaque mois
    data = [consultations.filter(date__month=i).count() for i in range(1, 13)]
    data_physique = [consultations.filter(date__month=i, type_consultation='physique').count() for i in range(1, 13)]
    data_numerique = [consultations.filter(date__month=i, type_consultation='numerique').count() for i in range(1, 13)]

    context = {
        'fiche': fiche,
        'consultation_labels': labels,
        'consultation_data': data,
        'consultation_data_physique': data_physique,
        'consultation_data_numerique': data_numerique,
    }

    return render(request, 'ficheapp/fiche_detail2.html', context)






def fiche_create(request):
    if request.method == 'POST':
        form = FicheForm(request.POST, request.FILES)  # Ajout de request.FILES
        if form.is_valid():
            fiche = form.save()
            messages.success(request, 'La fiche a été créée avec succès.')
            return redirect('fiche_detail', fiche_id=fiche.id)
        else:
            messages.error(request, 'Il y a eu une erreur lors de la création de la fiche. Veuillez vérifier les informations fournies.')
    else:
        form = FicheForm()
    return render(request, 'ficheapp/fiche_form.html', {'form': form})

def consultation_create(request, fiche_id):
    fiche = get_object_or_404(Fiche, id=fiche_id)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.fiche = fiche
            consultation.save()
            messages.success(request, 'La consultation a été créée avec succès.')
            return redirect('fiche_detail', fiche_id=fiche.id)
        else:
            messages.error(request, 'Il y a eu une erreur lors de la création de la consultation. Veuillez vérifier les informations fournies.')
            print(form.errors)  # Décommenter pour le débogage uniquement
    else:
        form = ConsultationForm()
    return render(request, 'ficheapp/consultation_form.html', {'form': form, 'fiche': fiche})

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
    return render(request, 'ficheapp/impExpcote.html')

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
    return render(request, 'ficheapp/importDiscipline.html')


def statistics_view(request):
    return render(request, 'ficheapp/statistics.html')

def get_statistics_data(request):
    data = Fiche.objects.annotate(month=TruncMonth('created_at')).values('month', 'annee_academique', 'promotion_filiere', 'genre').annotate(total=Count('id'))
    return JsonResponse(list(data), safe=False)



def monthly_consultations_statistics(request):
    # Initialisation des statistiques
    stats = defaultdict(lambda: {'M': [0] * 12, 'F': [0] * 12, 'total_M': 0, 'total_F': 0})

    # Récupération de toutes les fiches
    fiches = Fiche.objects.all()

    for fiche in fiches:
        consultations = fiche.consultations.all()
        for consultation in consultations:
            month = consultation.date.month - 1  # Les index des mois vont de 0 à 11
            promotion = fiche.promotion_filiere
            genre = fiche.genre
            if genre in stats[promotion]:
                stats[promotion][genre][month] += 1
                stats[promotion][f'total_{genre}'] += 1

    # Générer des labels pour tous les mois
    labels = [calendar.month_abbr[i] for i in range(1, 13)]

    context = {
        'stats': dict(stats),
        'labels': labels,
    }

    return render(request, 'ficheapp/monthly_consultations_statistics.html', context)