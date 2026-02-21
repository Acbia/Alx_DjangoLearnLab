from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.services import create_notification

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class ApiRootView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {
                "message": "Social Media API is running.",
                "endpoints": {
                    "register": request.build_absolute_uri(reverse("register")),
                    "login": request.build_absolute_uri(reverse("login")),
                    "profile": request.build_absolute_uri(reverse("profile")),
                },
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FollowUserView(APIView):
    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if target_user.followers.filter(id=request.user.id).exists():
            return Response({"detail": "Already following this user."}, status=status.HTTP_200_OK)

        target_user.followers.add(request.user)
        create_notification(
            recipient=target_user,
            actor=request.user,
            verb="started following you",
            target=request.user,
        )
        return Response({"detail": "Now following this user."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        if target_user == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not target_user.followers.filter(id=request.user.id).exists():
            return Response(
                {"detail": "You are not following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_user.followers.remove(request.user)
        return Response({"detail": "Unfollowed this user."}, status=status.HTTP_200_OK)
