from rest_framework import serializers
from accounts.serializers import UserMiniSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    user=UserMiniSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]