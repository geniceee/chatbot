from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from .models import Chat, Contact, Message
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

User = get_user_model()

def login_redirect(request):
    return HttpResponseRedirect('accounts/login/')

def index(request):

    queryset = Chat.objects.all()
    author = request.user.username
    contact = get_user_contact(author)
    queryset = contact.chats.all()
    chats = queryset.values()

    context = {
        'username': mark_safe(json.dumps(request.user.username)),
        'filtered_chats': chats,
    }

    return render(request, 'chat/index.html', context=context)

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)

@login_required
def room(request, room_name):

    queryset = Chat.objects.all()
    print(queryset)
    author = request.user.username
    contact = get_user_contact(author)
    queryset = contact.chats.all()
    chats = queryset.values()


    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'filtered_chats': chats,

    }

    return render(request, 'chat/room.html', context=context)

def get_last_10_messages(room_name):
    chat = get_object_or_404(Chat, id=room_name)
    return chat.messages.order_by('-timestamp').all()[:10]

def get_current_chat(room_name):
    return get_object_or_404(Chat, id=room_name)



