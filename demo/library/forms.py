from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'subtitle', 'category', 'description', 'total_copies', 'author', 'isbn']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'placeholder': 'Enter book title'
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'placeholder': 'Enter subtitle'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'rows': 4,
                'placeholder': 'Enter book description'
            }),
            'total_copies': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'placeholder': 'Total copies available'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'placeholder': 'Author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2',
                'placeholder': 'ISBN number'
            }),
        }
