from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

post_like = PostViewSet.as_view({"post": "like"})
post_unlike = PostViewSet.as_view({"post": "unlike"})

urlpatterns = [
    path("posts/<int:pk>/like/", post_like, name="post-like"),
    path("posts/<int:pk>/unlike/", post_unlike, name="post-unlike"),
    path("", include(router.urls)),
]
