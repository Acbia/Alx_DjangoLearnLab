from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Post

User = get_user_model()


class PostCommentApiTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="author1",
            email="author1@example.com",
            password="strongpass123",
        )
        self.user2 = User.objects.create_user(
            username="author2",
            email="author2@example.com",
            password="strongpass123",
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def _auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_post(self):
        self._auth(self.token1)
        payload = {"title": "First Post", "content": "My first post content"}
        response = self.client.post("/api/posts/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "author1")

    def test_post_update_delete_permission_enforced(self):
        post = Post.objects.create(
            author=self.user1,
            title="Protected Post",
            content="Only author can edit",
        )

        self._auth(self.token2)
        update_response = self.client.patch(
            f"/api/posts/{post.id}/",
            {"title": "Hacked"},
            format="json",
        )
        delete_response = self.client.delete(f"/api/posts/{post.id}/")

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_and_pagination_for_posts(self):
        for i in range(12):
            Post.objects.create(
                author=self.user1,
                title=f"Searchable Post {i}",
                content="keyword only in these posts",
            )

        self._auth(self.token1)
        response = self.client.get("/api/posts/?search=keyword")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 10)

    def test_create_comment_and_comment_permissions(self):
        post = Post.objects.create(author=self.user1, title="Post", content="Text")

        self._auth(self.token1)
        create_response = self.client.post(
            "/api/comments/",
            {"post": post.id, "content": "Nice post"},
            format="json",
        )
        comment_id = create_response.data["id"]
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["author"], "author1")

        self._auth(self.token2)
        update_response = self.client.patch(
            f"/api/comments/{comment_id}/",
            {"content": "Edited by someone else"},
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
