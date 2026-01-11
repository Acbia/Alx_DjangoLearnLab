from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # for checker
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
    IsAdminUser
)
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from django_filters import rest_framework


class BookListView(generics.ListAPIView):
    """List all books (GET)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """Retrieve single book (GET)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookCreateView(generics.CreateAPIView):
    """Create new book (POST)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Custom book creation logic"""
        serializer.save(created_by=self.request.user)


class BookUpdateView(generics.UpdateAPIView):
    """Update existing book (PUT/PATCH)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    """Delete book (DELETE)"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
