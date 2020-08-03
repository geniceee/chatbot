from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from .models import Message, Chat, Contact
# from .forms import DocumentForm
from django.contrib.auth import get_user_model
from datetime import datetime

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

# def check_profile(func):
#     def decorator(func):
#     # @wraps(func)
#         def wrapper(arg_1, arg_2):
#             context = {
#             'room_name_json': mark_safe(json.dumps(arg_2)),
#             }
#             requested_chat = Chat.objects.get(id=arg_2)
#             query_participants = requested_chat.participants.all()
#             count = 0
#             for participant in query_participants:
#                 user = request.user.username
#                 participant_name = participant.user.username
#                 if user == participant_name:
#                     count += 1
#             if count==0:
#                 logout(request)
#                 return HttpResponseRedirect('/accounts/logout/')
#             return wrapper
#         return decorator

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

    msg_list= []

    for chat in queryset:
        msg_list = chat.messages.order_by('-timestamp').all()
        last_msg_author = msg_list[0]
        last_msg = last_msg_author.content
    
    context = {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'filtered_chats': queryset,
        'author': author,
        'messages': msg_list
    }

    return render(request, 'chat/room.html', context=context)

# def room(request, room_name):
#     queryset = Chat.objects.all()
#     author = request.user.username
#     contact = get_user_contact(author)
#     queryset = contact.chats.all()
#     chats = queryset.values()

#     context = {
#         'room_name_json': mark_safe(json.dumps(room_name)),
#         'username': mark_safe(json.dumps(request.user.username)),
#         'filtered_chats': chats,
#     }

#     return render(request, 'chat/room.html', context=context)


def get_last_10_messages(room_name):
    chat = get_object_or_404(Chat, id=room_name)
    return chat.messages.order_by('-timestamp').all()

def get_current_chat(room_name):
    return get_object_or_404(Chat, id=room_name)

# def image_view(request):
#     # Handle file upload
#     print('success')
#     if request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile = request.FILES['docfile'])
#             newdoc.save()
#             return redirect('success') 
#     else: 
#         form = DocumentForm() 
#     return render(request, 'room.html', {'form' : form}) 
  
  
# def success(request): 
#     return HttpResponse('successfully uploaded') 

def profile_photo(request):
    data=request.FILES.get('file')

    author = request.user.username
    if author.profile_photo:
        authpath = author.profile_photo.url.split(settings.MEDIA_URL)
        os.remove(os.path.join(settings.MEDIA_ROOT,authpath[1]))
    #data.name = str(request.user.id) + "_apfp"
    author.profile_photo=data
    author.save()

    data = {
        'ok' : 'ok',
    }
    return JsonResponse(data)