from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Fiche, Consultation
from .forms import FicheForm, ConsultationForm

def fiche_list(request):
    fiches = Fiche.objects.all()
    return render(request, 'ficheapp/fiche_list.html', {'fiches': fiches})

def fiche_detail(request, fiche_id):
    fiche = get_object_or_404(Fiche, id=fiche_id)
    return render(request, 'ficheapp/fiche_detail2.html', {'fiche': fiche})

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
