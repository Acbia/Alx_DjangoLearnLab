from rest_framework import serializers
from .models import Post, Comment, Like
from django.conf import settings

class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'user_username', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'author_username', 'author_profile_picture', 
                 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')
    
    def get_author_profile_picture(self, obj):
        if obj.author.profile_picture:
            return obj.author.profile_picture.url
        return None

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_profile_picture = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_author_following = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'author', 'author_username', 'author_profile_picture', 
                 'title', 'content', 'created_at', 'updated_at', 
                 'comments_count', 'likes_count', 'comments', 
                 'is_author_following', 'is_liked')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at', 
                          'comments_count', 'likes_count')
    
    def get_comments_count(self, obj):
        return obj.comments_count()
    
    def get_author_profile_picture(self, obj):
        if obj.author.profile_picture:
            return obj.author.profile_picture.url
        return None
    
    def get_is_author_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj.author)
        return False
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False