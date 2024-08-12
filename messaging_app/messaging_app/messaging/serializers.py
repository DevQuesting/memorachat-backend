from rest_framework import serializers
from .models import Chat, Message, Profile, Notification
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    class Meta:
        model = Chat
        fields = ['id', 'participants', 'is_group_chat', 'group_name', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp', 'is_favorited', 'is_read', 'image', 'file']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'