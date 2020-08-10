from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from .models import Chat, Contact, Message
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from chatbot import settings
import os
from django.http import JsonResponse

User = get_user_model()

def login_redirect(request):
    return HttpResponseRedirect('accounts/login/')

def index(request):

    queryset = Chat.objects.all()
    author = request.user.username
    contact = get_user_contact(author)
    queryset = contact.chats.all()

    context = {
        'filtered_chats': queryset,
        'author': author,
        'contact': contact,
    }

    return render(request, 'chat/index.html', context=context)

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Contact, user=user)


def check_profile(func):
    def wrapper(request, room_name):
        context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        }
        requested_chat = Chat.objects.get(id=room_name)
        query_participants = requested_chat.participants.all()
        count = 0
        for participant in query_participants:
            user = request.user.username
            participant_name = participant.user.username
            if user == participant_name:
                count += 1
        if count==0:
            # logout(request)
            return HttpResponseRedirect('/accounts/logout/')
        
        return func(request, room_name)
    return wrapper


@login_required
@check_profile
def room(request, room_name):

    queryset = Chat.objects.all()
    author = request.user.username
    contact = get_user_contact(author)
    queryset = contact.chats.all()

    requested_chat = Chat.objects.get(id=room_name)
    query_participants = requested_chat.participants.all()

    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'filtered_chats': queryset,
        'author': author,
        'contact': contact,
        'participants': query_participants
    }

    return render(request, 'chat/room.html', context=context)

def get_last_10_messages(room_name):
    chat = get_object_or_404(Chat, id=room_name)
    return chat.messages.order_by('timestamp').all()

def get_current_chat(room_name):
    return get_object_or_404(Chat, id=room_name)

def profile_photo(request):
    data=request.FILES.get('file')

    user = request.user
    author = Contact.objects.get(user=user)

    if author.msg_file:
        advpath = author.msg_file.url.split(settings.MEDIA_URL)
        os.remove(os.path.join(settings.MEDIA_ROOT,advpath[1]))
    
    # data.name = str(request.user.id) + "_apfp"
    author.msg_file=data
    author.save()

    data = {
        'ok' : 'ok',
    }
    return JsonResponse(data)



