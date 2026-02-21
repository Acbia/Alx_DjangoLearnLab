from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Notification

User = get_user_model()


class NotificationApiTests(APITestCase):
    def setUp(self):
        self.recipient = User.objects.create_user(
            username="recipient",
            email="recipient@example.com",
            password="strongpass123",
        )
        self.actor = User.objects.create_user(
            username="actor",
            email="actor@example.com",
            password="strongpass123",
        )
        self.other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="strongpass123",
        )
        self.token = Token.objects.create(user=self.recipient)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_list_notifications_returns_only_current_users_notifications(self):
        unread = Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            verb="liked your post",
            is_read=False,
        )
        read = Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            verb="commented on your post",
            is_read=True,
        )
        Notification.objects.create(
            recipient=self.other,
            actor=self.actor,
            verb="started following you",
            is_read=False,
        )

        response = self.client.get("/notifications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(response.data["results"][0]["id"], unread.id)
        self.assertEqual(response.data["results"][1]["id"], read.id)

    def test_mark_notification_as_read(self):
        notification = Notification.objects.create(
            recipient=self.recipient,
            actor=self.actor,
            verb="liked your post",
            is_read=False,
        )

        response = self.client.post(f"/notifications/{notification.id}/read/")
        notification.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(notification.is_read)
