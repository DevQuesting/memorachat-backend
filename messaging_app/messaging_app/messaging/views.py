#from django.shortcuts import render

# Create your views here.

# messaging/views.py

from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from django.contrib.auth.models import User

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @action(detail=False, methods=['post'])
    def create_chat(self, request):
        participants = request.data.get('participants', [])
        is_group_chat = request.data.get('is_group_chat', False)
        group_name = request.data.get('group_name', '')

        if not participants:
            return Response({"error": "Participants list cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        if is_group_chat and not group_name:
            return Response({"error": "Group name is required for group chats."}, status=status.HTTP_400_BAD_REQUEST)

        chat = Chat.objects.create(is_group_chat=is_group_chat, group_name=group_name)

        for participant_id in participants:
            user = User.objects.get(id=participant_id)
            chat.participants.add(user)

        chat.save()
        return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Chat, Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat = Chat.objects.get(pk=pk)
        sender = request.user
        content = request.data.get('content', '')

        if not content:
            return Response({"error": "Message content cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(chat=chat, sender=sender, content=content)
        message.save()

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_messages(self, request, pk=None):
        chat = Chat.objects.get(pk=pk)
        messages = chat.message_set.all()  # Retrieve all messages for this chat
        return Response(MessageSerializer(messages, many=True).data)


# messaging/views.py

from rest_framework import generics
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(['GET'])
def global_search(request):
    query = request.query_params.get('q', '')

    if query:
        # Search for users
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))

        # Search for messages
        messages = Message.objects.filter(Q(content__icontains=query))

        # Search for chats by group name or participants
        chats = Chat.objects.filter(
            Q(group_name__icontains=query) | Q(participants__username__icontains=query)
        ).distinct()

        user_data = [{'id': user.id, 'username': user.username} for user in users]
        message_data = MessageSerializer(messages, many=True).data
        chat_data = ChatSerializer(chats, many=True).data

        return Response({
            'users': user_data,
            'messages': message_data,
            'chats': chat_data
        })
    else:
        return Response({"error": "Query parameter is missing"}, status=400)
