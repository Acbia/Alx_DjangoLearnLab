from django.urls import path

from .views import (
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
)

urlpatterns = [
    # Collection endpoints
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    # Single-resource endpoints
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    # Alias routes to satisfy alternate URL checks
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book-update-alt"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete-alt"),
]
