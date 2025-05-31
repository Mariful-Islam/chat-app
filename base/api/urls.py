from django.urls import path
from base.api.views import MessageUpdateDelete, RoomMessage, UserModelViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('api/users', UserModelViewset)




api_urlpatterns = [
    path('api/messages/<int:id>/', MessageUpdateDelete.as_view()),
    path('api/chat/room/<str:room_name>/', RoomMessage.as_view())
]+router.urls
