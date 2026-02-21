from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response

from notifications.services import create_notification

from .models import Comment, Like, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author").prefetch_related("comments", "likes").all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if getattr(self, "action", None) in {"like", "unlike"}:
            return [permissions.IsAuthenticated()]
        return [permission() for permission in self.permission_classes]

    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if created:
            create_notification(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
            )
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

        return Response({"detail": "Post already liked."}, status=status.HTTP_200_OK)

    def unlike(self, request, pk=None):
        post = self.get_object()
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()

        if not deleted:
            return Response({"detail": "Post was not liked."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post").all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        create_notification(
            recipient=comment.post.author,
            actor=self.request.user,
            verb="commented on your post",
            target=comment,
        )
