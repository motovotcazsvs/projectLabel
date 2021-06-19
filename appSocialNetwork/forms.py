from django import forms 
from .models import Book

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        #fields - для создания обьекта на сайте
        fields = ('title_book', 'author_book', 'date_book', 'description_book', 'image_book', 
        'pdf_book')


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
        