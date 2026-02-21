from django.urls import path

from .views import (
    ApiRootView,
    FollowUserView,
    LoginView,
    ProfileView,
    RegisterView,
    UnfollowUserView,
)

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("users/<int:user_id>/follow/", FollowUserView.as_view(), name="follow-user"),
    path("users/<int:user_id>/unfollow/", UnfollowUserView.as_view(), name="unfollow-user"),
]
