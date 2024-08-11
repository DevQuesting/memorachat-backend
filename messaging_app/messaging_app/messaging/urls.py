# messaging/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ChatViewSet, MessageViewSet, global_search

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'chats', ChatViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/', global_search, name='global_search'),
]