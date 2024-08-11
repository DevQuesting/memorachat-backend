from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
    


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    is_group_chat = models.BooleanField(default=False)
    group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_group_chat:
            return f"Group: {self.group_name}"
        else:
            return f"Chat between {self.participants.all()[0]} and {self.participants.all()[1]}"




class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_favorited = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

