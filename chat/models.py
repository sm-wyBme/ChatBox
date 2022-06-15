from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#chat message
class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)

    def __str__(self):
        return f'Logs_{self.room}'


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name