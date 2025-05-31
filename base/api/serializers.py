from base.models import Message
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"



class RoomMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"