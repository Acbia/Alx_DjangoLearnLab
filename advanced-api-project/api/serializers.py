from datetime import date

from rest_framework import serializers

from .models import Author, Book


# BookSerializer exposes all Book fields and adds validation for publication_year.
class BookSerializer(serializers.ModelSerializer):
    # Ensure the publication year is not in the future.
    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "publication_year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = "__all__"


# AuthorSerializer exposes the Author name and nests the related books.
# The relationship is handled via Book.author -> Author (one-to-many) using
# the related_name="books" declared on the Book model.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serialization of all books for this author (read-only by default).
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
