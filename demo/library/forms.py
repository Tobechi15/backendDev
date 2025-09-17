from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your review..."}),
        }

class BorrowBookForm(forms.Form):
    member_id = forms.IntegerField(label="Member ID")
    book_id = forms.IntegerField(label="Book ID")

class ReturnBookForm(forms.Form):
    record_id = forms.IntegerField(label="Borrow Record ID")
