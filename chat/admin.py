from django.contrib import admin

# Register your models here.
# from .models import Message

# admin.site.register(Message) 
from .models import Chat, Contact, Message, File, Notification

admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message) 
admin.site.register(File) 
admin.site.register(Notification)