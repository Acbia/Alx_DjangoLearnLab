from django import forms
from .models import Book
from .forms import ExampleForm


class BookSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, strip=True)
    
class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn']
        
