from django import forms
from .models import Book, Record

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []

