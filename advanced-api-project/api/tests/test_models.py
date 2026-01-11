from django.test import TestCase
from .models import Author, Book

class ModelTests(TestCase):
    def test_author_creation(self):
        author = Author.objects.create(name="Test Author")
        self.assertEqual(str(author), "Test Author")

    def test_book_creation(self):
        author = Author.objects.create(name="Test Author")
        book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=author
        )
        self.assertEqual(str(book), "Test Book by Test Author (2023)")