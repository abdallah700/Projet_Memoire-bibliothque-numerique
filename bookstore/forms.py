from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bookstore.models import Chat, Book
from django import forms
from .models import Book, CoteLivre


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message', )


class BookForm(forms.ModelForm):
    cote_book = forms.ModelChoiceField(queryset=CoteLivre.objects.all(), empty_label="Select Cote Livre")

    class Meta:
        model = Book
        fields = ('title', 'author', 'nbr_exemplaire', 'cote_book', 'num_invetaire', 'publisher', 'year', 'uploaded_by', 'desc', 'cover', 'pdf')
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class CoteLivreForm(forms.ModelForm):
    class Meta:
        model = CoteLivre
        fields = '__all__'