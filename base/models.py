from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200)
    users_online = models.ManyToManyField(User,  related_name='users_online', blank=True, null=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True, null=True)
    is_private = models.BooleanField(default=False)



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_msg')

    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.text}'

