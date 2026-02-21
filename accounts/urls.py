from django.urls import path

from .views import ApiRootView, LoginView, ProfileView, RegisterView

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("profile", ProfileView.as_view(), name="profile"),
]
