from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('chat/<str:username>/', views.get_or_create_chatroom, name='chat'),
    path('chat/room/<str:room_name>/', views.chat_room, name='chat_room'),
    path('users/', views.user_list, name='user_list'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),



    path('chat-delete-all/<str:room_name>/', views.chat_delete_all, name='chat_delete_all'),
    path('chat_delete_one_by_one/<str:room_name>/<int:message_id>/', views.chat_delete_one_by_one, name='chat_delete_one_by_one'),


]


