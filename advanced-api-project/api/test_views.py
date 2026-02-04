from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookApiTests(APITestCase):
    """End-to-end tests for Book API endpoints, permissions, and query features."""

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@example.com", password="pass1234"
        )
        self.author = Author.objects.create(name="Ursula K. Le Guin")
        self.book1 = Book.objects.create(
            title="A Wizard of Earthsea",
            publication_year=1968,
            author=self.author,
        )
        self.book2 = Book.objects.create(
            title="The Tombs of Atuan",
            publication_year=1971,
            author=self.author,
        )

    # ---- Read endpoints (public) ----
    def test_list_books_public(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_detail_book_public(self) -> None:
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.pk)

    # ---- Write endpoints (auth required) ----
    def test_create_book_requires_auth(self) -> None:
        url = reverse("book-create")
        payload = {
            "title": "The Farthest Shore",
            "publication_year": 1972,
            "author": self.author.pk,
        }
        response = self.client.post(url, payload, format="json")
        self.assertIn(
            response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])

    def test_update_book_requires_auth(self) -> None:
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        payload = {
            "title": "A Wizard of Earthsea (Updated)",
            "publication_year": 1968,
            "author": self.author.pk,
        }
        response = self.client.put(url, payload, format="json")
        self.assertIn(
            response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, payload["title"])

    def test_delete_book_requires_auth(self) -> None:
        url = reverse("book-delete", kwargs={"pk": self.book2.pk})
        response = self.client.delete(url)
        self.assertIn(
            response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ---- Filtering / searching / ordering ----
    def test_filter_by_title(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url, {"title": "A Wizard of Earthsea"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "A Wizard of Earthsea")

    def test_search_by_author_name(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Le Guin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_ordering_by_publication_year(self) -> None:
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item["publication_year"] for item in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
