from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
import datetime


class BookAPITests(APITestCase):
    """Test suite for the Book API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        self.book1 = Book.objects.create(
            title="Alpha Book",
            publication_year=2001,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Beta Book",
            publication_year=2010,
            author=self.author2
        )

        self.list_url = reverse("book-list")   
        self.detail_url = lambda pk: reverse("book-detail", args=[pk]) 

    def test_list_books(self):
        """Test that anyone can list books."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Test that anyone can retrieve a single book."""
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "Gamma Book",
            "publication_year": 2022,
            "author": self.author1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2022,
            "author": self.author1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Test that authenticated users can update books."""
        self.client.login(username="testuser", password="testpass123")
        data = {
            "title": "Updated Alpha Book",
            "publication_year": 2001,
            "author": self.author1.id
        }
        response = self.client.put(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Alpha Book")

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """Test filtering books by author name."""
        url = f"{self.list_url}?author__name=Author One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha Book")

    def test_search_books(self):
        """Test searching books by title."""
        url = f"{self.list_url}?search=Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha Book")

    def test_order_books_by_title(self):
        """Test ordering books by title."""
        url = f"{self.list_url}?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_validate_future_publication_year(self):
        """Test that creating a book with a future year fails validation."""
        self.client.login(username="testuser", password="testpass123")
        next_year = datetime.datetime.now().year + 1
        data = {
            "title": "Future Book",
            "publication_year": next_year,
            "author": self.author1.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
