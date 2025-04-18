from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as user_logout

from .models import Message, Room
from django.db.models import Q



User = get_user_model()

# Create your views here.


def home(req):
    if req.user.is_authenticated:
        return redirect('user_list')
    
    
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
   

                return redirect('user_list')
            else:
                return redirect('login')
            


    return render(request, 'login.html')        


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            user.save()

            return redirect('login')


    return render(request, 'signup.html')        


def user_list(request):
    users = User.objects.all().exclude(id = request.user.id)

    rooms = Room.objects.filter(members=request.user)

    return render(request, 'user.html', {"users": users, "me": request.user, "rooms": rooms})




def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('user_list')

    other_user = get_object_or_404(User, username=username)

    # Find existing private chatrooms involving the current user
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    # Try to find a room with both users
    for chatroom in my_chatrooms:
        if chatroom.members.filter(id=other_user.id).exists():
            return redirect('chat_room', chatroom.name)

    # No existing room, so create a new one
    room_name = f'chat_{min(request.user.username, other_user.username)}_{max(request.user.username, other_user.username)}'
    new_chatroom = Room.objects.create(is_private=True, name=room_name)
    new_chatroom.members.add(request.user, other_user)

    return redirect('chat_room', new_chatroom.name)

        



def chat_room(request, room_name):
    
    room = get_object_or_404(Room, name=room_name)

    other_user = room.members.exclude(id=request.user.id)[0]

    messages = Message.objects.filter(room=room)


    return render(request, 'chat.html', {"room_name": room_name, "receiver": other_user.username, "messages": messages })



def chat_delete_all(request, room_name):
    room = get_object_or_404(Room, name=room_name)

    messages = Message.objects.filter(room=room)
    messages.delete()

    return redirect('chat_room', room_name)


def chat_delete_one_by_one(request, room_name, message_id):
    room = get_object_or_404(Room, name=room_name)

    messages = Message.objects.get(room=room, id=message_id)
    messages.delete()

    return redirect('chat_room', room_name)


def logout(request):
    user_logout(request)
    return redirect('login')
