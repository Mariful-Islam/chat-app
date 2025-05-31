from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from base.models import Message, Room
from base.api.serializers import MessageSerializer, RoomMessageSerializer, UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class MessageUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'id'



class RoomMessage(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = RoomMessageSerializer

    def get_queryset(self):
        room_name = self.kwargs.get('room_name')

        room = get_object_or_404(Room, name=room_name)

        messages = Message.objects.filter(room=room)

        return messages
    

class UserModelViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        