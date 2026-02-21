from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from notifications.models import Notification

User = get_user_model()


class AuthenticationFlowTests(APITestCase):
    def test_register_returns_token(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpass123",
        }
        response = self.client.post("/register", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], payload["username"])

    def test_login_and_profile(self):
        register_payload = {
            "username": "loginuser",
            "email": "loginuser@example.com",
            "password": "strongpass123",
        }
        register_response = self.client.post("/register", register_payload, format="json")
        token = register_response.data["token"]

        login_response = self.client.post(
            "/login",
            {"username": "loginuser", "password": "strongpass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", login_response.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        profile_response = self.client.get("/profile")
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["username"], "loginuser")


class FollowFlowTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="follower",
            email="follower@example.com",
            password="strongpass123",
        )
        self.user2 = User.objects.create_user(
            username="target",
            email="target@example.com",
            password="strongpass123",
        )
        self.token1 = Token.objects.create(user=self.user1)

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

    def test_follow_and_unfollow_user(self):
        self._auth()
        follow_response = self.client.post(f"/users/{self.user2.id}/follow/")
        duplicate_follow_response = self.client.post(f"/users/{self.user2.id}/follow/")
        unfollow_response = self.client.post(f"/users/{self.user2.id}/unfollow/")

        self.assertEqual(follow_response.status_code, status.HTTP_200_OK)
        self.assertEqual(duplicate_follow_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unfollow_response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user2.followers.filter(id=self.user1.id).exists())

    def test_follow_creates_notification(self):
        self._auth()
        response = self.client.post(f"/users/{self.user2.id}/follow/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user2,
                actor=self.user1,
                verb="started following you",
            ).exists()
        )

    def test_follow_self_rejected(self):
        self._auth()
        response = self.client.post(f"/users/{self.user1.id}/follow/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
