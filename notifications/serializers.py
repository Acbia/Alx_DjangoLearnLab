from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor",
            "actor_username",
            "verb",
            "target_type",
            "target_id",
            "target_repr",
            "is_read",
            "timestamp",
        ]
        read_only_fields = fields

    def get_target_type(self, obj):
        return obj.content_type.model if obj.content_type else None

    def get_target_id(self, obj):
        return obj.object_id

    def get_target_repr(self, obj):
        return str(obj.target) if obj.target else None
