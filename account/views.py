# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import BibliothecaireForm, EtudiantInterneForm, LoginForm, AutrePersonneScientifiqueForm, FiliereForm, FaculteForm, PromotionForm, CategorieScientifiqueForm, Annee_academiqueForm
from .models import Bibliothecaire, EtudiantInterne, AutrePersonneScientifique,Filiere,Faculte, Promotion, CategorieScientifique, Annee_academique

def signin_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = None
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                # Redirect to a specific page after successful login
                return redirect('CategorSc_form')  # Change 'home' to the desired URL name
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'account/CategorieScientifique.html', {'CategorSc_form': form})

def signupAutrSc_view(request):
    if request.method == 'POST':
        form = AutrePersonneScientifiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signupAS')  # Replace with your success page
    else:
        form = AutrePersonneScientifiqueForm()
    # Votre logique de vue pour la page de connexion (signupAutre personne Scientifique )
    return render(request, 'account/signupAutrSc.html', {'AutreSc_form': form})

def signupBiblioth_view(request):
    if request.method == 'POST':
        form = BibliothecaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace with your success page
    else:
        form = BibliothecaireForm()
    # Votre logique de vue pour la page de connexion (signupAutre personne Scientifique )
    return render(request, 'account/signupBiblioth.html', {'Bibliotheque_form': form})


def signupEtInterne_view(request):
    if request.method == 'POST':
        form = EtudiantInterneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signupEtInt')  # Replace with your success page
    else:
        form = EtudiantInterneForm()
    return render(request, 'account/signupEtInterne.html', {'EtudiantInterne_form': form})


def Filiere_view(request):
    if request.method == 'POST':
        form = FiliereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Filiere')  # Replace with your success page
    else:
        form = FiliereForm()
    # Votre logique de vue pour la page de connexion (sign-in)
    return render(request, 'account/Filiere.html', {'Filiere_form': form})

def Faculte_view(request):
    if request.method == 'POST':
        form = FaculteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Faculte')  # Replace with your success page
    else:
        form = FaculteForm()
    # Votre logique de vue pour la page de connexion (signupAutre personne Scientifique )
    return render(request, 'account/FaculteForm.html', {'Faculte_form': form})

def Promotion_view(request):
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Promotion')  # Replace with your success page
    else:
        form = PromotionForm()
    # Votre logique de vue pour la page de connexion (signupAutre personne Scientifique )
    return render(request, 'account/Promotion.html', {'Promotion_form': form})


def CategorieScientifique_view(request):
    if request.method == 'POST':
        form = CategorieScientifiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('CategorSc_form')  # Replace with your success page
    else:
        form = CategorieScientifiqueForm()
    return render(request, 'account/CategorieScientifique.html', {'CategorSc_form': form})

def Annee_academique_view(request):
    if request.method == 'POST':
        form = Annee_academiqueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Annee_academique')  # Replace with your success page
    else:
        form = Annee_academiqueForm()
    return render(request, 'account/Annee_academique.html', {'AnneAcad_form': form})
