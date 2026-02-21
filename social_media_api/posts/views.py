from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsOwnerOrReadOnly
from notifications.models import Notification


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )
            return Response({'status': 'success', 'message': 'Post liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'info', 'message': 'You already liked this post'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
            return Response({'status': 'success', 'message': 'Post unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
        likes = post.likes.all()
        page = self.paginate_queryset(likes)
        if page is not None:
            serializer = LikeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                content_type=ContentType.objects.get_for_model(comment.post),
                object_id=comment.post.id
            )

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    page = request.query_params.get('page', 1)
    page_size = request.query_params.get('page_size', 10)

    paginator = Paginator(posts, page_size)
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)

    serializer = PostSerializer(paginated_posts, many=True, context={'request': request})
    return Response({
        'count': paginator.count,
        'pages': paginator.num_pages,
        'current_page': int(page),
        'results': serializer.data
    })
