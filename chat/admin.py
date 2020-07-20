from django.contrib import admin

# Register your models here.
# from .models import Message

# admin.site.register(Message) 
from .models import Chat, Contact, Message

admin.site.register(Chat)
admin.site.register(Contact)
admin.site.register(Message) 