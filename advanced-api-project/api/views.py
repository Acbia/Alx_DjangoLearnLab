from django_filters import rest_framework
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Book
from .serializers import BookSerializer

# BookListView lists all books. It is public and supports basic search/ordering
# to demonstrate DRF filters on a generic view.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    # Read-only for unauthenticated users; write requires authentication.
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Filtering, searching, and ordering for advanced queries.
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title", "publication_year", "author", "author__name"]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year"]
    ordering = ["id"]


# BookDetailView retrieves a single book by primary key. It is public.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# BookCreateView creates a new book. It requires authentication.
# DRF handles form data parsing and serializer validation before save().
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer: BookSerializer) -> None:
        # Hook for custom behavior; serializer validation runs before this.
        serializer.save()


# BookUpdateView updates an existing book. It requires authentication.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer: BookSerializer) -> None:
        # Hook for custom behavior; serializer validation runs before this.
        serializer.save()


# BookDeleteView deletes an existing book. It requires authentication.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
