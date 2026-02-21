from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    actor_profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'actor_username', 'actor_profile_picture',
                 'verb', 'target', 'is_read', 'created_at')
        read_only_fields = ('id', 'recipient', 'actor', 'created_at')
    
    def get_actor_profile_picture(self, obj):
        if obj.actor.profile_picture:
            return obj.actor.profile_picture.url
        return None