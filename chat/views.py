from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from .models import Chat, Contact, Message, File
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponseRedirect
from chatbot import settings
import os
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.urls import reverse


User = get_user_model()

def login_redirect(request):
    return HttpResponseRedirect('accounts/login/')

@receiver(post_save, sender= User)
def create_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance)

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

# def sign_up(request):
#     context = {}
#     form = UserCreationForm(request.POST or None)
#     if request.method == "POST":
#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             return render(request,'chat/index.html')
#     context['form']=form
#     return render(request,'chat/sign_up.html', context)    

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

def all_users(request):

    author = request.user.username
    contact = get_user_contact(author)

    contacts = Contact.objects.all()

    context= {
        'author': author,
        'contact': contact,
        'contacts': contacts,
    }

    return render(request, 'chat/all_users.html', context=context)


def get_last_10_messages(room_name):
    chat = get_object_or_404(Chat, id=room_name)
    return chat.messages.order_by('timestamp').all()

def get_current_chat(room_name):
    return get_object_or_404(Chat, id=room_name)

def create_chat(request, second_user_id):

    first_contact = Contact.objects.get(user=request.user)
    second_contact = Contact.objects.get(id=second_user_id)

    existing = Chat.objects.filter(participants=first_contact.id).filter(participants=second_contact.id)

    if existing.exists():
        return redirect(reverse('room', kwargs={'room_name': existing[0].id}))
    else:
        chat = Chat.objects.create()
        chat.participants.set([first_contact, second_contact])
        chat.save()

        return redirect(reverse('room', kwargs={'room_name': existing[0].id}))


def profile_photo(request):
    data=request.FILES.get('file') 

    user_id = request.user.id

    author = Contact.objects.get(id=user_id)

    # removes the image
    if author.profile_photo:
        advpath = author.profile_photo.url.split(settings.MEDIA_URL)
        print(advpath)
        os.remove(os.path.join(settings.MEDIA_ROOT,advpath[1]))
    author.profile_photo=data
    author.save()
    print(author.profile_photo)

    data = {
        'ok' : 'ok',
    }
    return JsonResponse(data)

def upload_file(request):
    data=request.FILES.get('file')
    existing_ids = list(File.objects.values_list('id', flat=True).order_by('id'))

    for file_id in range(1, 100):
        if file_id not in existing_ids:
            existing_ids.append(file_id)
            file_obj = File.objects.create(id=file_id)
            break
        else:
            file_id += 1

    # removes the image
    if file_obj.attachment:
        advpath = file_obj.attachment.url.split(settings.MEDIA_URL)
        os.remove(os.path.join(settings.MEDIA_ROOT,advpath[1]))
    file_obj.attachment=data
    file_obj.save()

    data = {
        'filepath' : file_obj.attachment.url,
    }

    # print(data['filepath'])
    return JsonResponse(data)


