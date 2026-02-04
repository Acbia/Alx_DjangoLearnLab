from rest_framework import filters, generics, permissions

from .models import Book
from .serializers import BookSerializer

# BookListView lists all books. It is public and supports basic search/ordering
# to demonstrate DRF filters on a generic view.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    # Read-only for unauthenticated users; write requires authentication.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year"]
    ordering = ["id"]


# BookDetailView retrieves a single book by primary key. It is public.
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# BookCreateView creates a new book. It requires authentication.
# DRF handles form data parsing and serializer validation before save().
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer: BookSerializer) -> None:
        # Hook for custom behavior; serializer validation runs before this.
        serializer.save()


# BookUpdateView updates an existing book. It requires authentication.
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer: BookSerializer) -> None:
        # Hook for custom behavior; serializer validation runs before this.
        serializer.save()


# BookDeleteView deletes an existing book. It requires authentication.
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
