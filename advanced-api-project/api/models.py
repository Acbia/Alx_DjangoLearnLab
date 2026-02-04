from django.db import models

# Author represents a single writer. A single Author can be linked to many Book
# records through the Book.author foreign key (one-to-many relationship).
class Author(models.Model):
    # Human-readable author name.
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


# Book represents a published work. Each Book must belong to exactly one Author.
class Book(models.Model):
    # Title of the book.
    title = models.CharField(max_length=255)
    # Year the book was published (stored as an integer for easy validation/filtering).
    publication_year = models.IntegerField()
    # Foreign key creates the one-to-many relationship to Author.
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
