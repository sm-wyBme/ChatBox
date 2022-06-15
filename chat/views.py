from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.http import HttpResponse

# Create your views here.

#Index page 
class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chat/index.html')

#Room page
class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):

        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []

        if room:
            chats = Chat.objects.filter(room=room)
        else:
            room = ChatRoom(name=room_name)
            room.save()

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'chats': chats,
        })