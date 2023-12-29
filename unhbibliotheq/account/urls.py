from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='account'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home')
]