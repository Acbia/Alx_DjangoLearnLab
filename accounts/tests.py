from rest_framework import status
from rest_framework.test import APITestCase


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

# Create your tests here.
