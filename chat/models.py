from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.core.files.storage import FileSystemStorage

# Create your models here.
User = get_user_model()

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    profile_photo = models.FileField(blank=True, null=True, upload_to='profilepic', storage=FileSystemStorage())

    def __str__(self):
        return self.user.username

class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(blank=True,null=True,storage=FileSystemStorage())
    attachmentName = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.contact.user.username

class File(models.Model):
    attachment = models.FileField(blank=True,null=True,
        upload_to='attachment',storage=FileSystemStorage())

    def __str__(self):
        return self.attachment.url

class Notification(models.Model):
    contact = models.ForeignKey(Contact, related_name='contacts', on_delete=models.CASCADE)
    message= models.ForeignKey(Message, related_name='msg_notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default= False)

    def __str__(self):
        return "{}".format(self.pk) 

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)
    notifications = models.ManyToManyField(Notification, blank=True)

    def __str__(self):
        return "{}".format(self.pk) 
    
    def most_recent_message(self):
        if self.messages.count() == 0:
            return None
        else:
            return self.messages.order_by('-timestamp').all()[0].content

    def most_recent_contact(self):
        return self.messages.order_by('-timestamp').all()[0].contact

    def other_contacts(self):
        return self.participants.all()

    def other_participants(self):
        return list(map(str,self.participants.all()))

    def get_absolute_url(self):
        return reverse('room', args=[str(self.pk)])

    def num_notifications(self):
        return self.notifications.filter(is_read=False).count()

