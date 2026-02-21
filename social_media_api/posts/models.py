from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def comments_count(self):
        return self.comments.count()
    
    likes_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def comments_count(self):
        return self.comments.count()
    
    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['user', 'post']  
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_likes_count()
    
    def delete(self, *args, **kwargs):
        post = self.post
        super().delete(*args, **kwargs)
        post.update_likes_count()