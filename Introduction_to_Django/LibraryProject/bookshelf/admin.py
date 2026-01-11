from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters on the sidebar
    list_filter = ('author', 'publication_year')
    
    # Add a search bar
    search_fields = ('title', 'author')
