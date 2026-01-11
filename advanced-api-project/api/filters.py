import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    publication_year = django_filters.NumberFilter(field_name='publication_year')
    publication_year__gt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='gt')
    publication_year__lt = django_filters.NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']