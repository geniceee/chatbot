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

    def __str__(self):
        return self.contact.user.username

    def render_timestamp(self):
        prefix = ""
        timeDiff = round(datetime.now.time() - self.timestamp.time() / 60000)

        if timeDiff < 1:
            prefix = "just now"
        elif timeDiff < 60 and timeDiff > 1:
            prefix = "{} minutes ago".format(timeDiff)
        elif timeDiff < 24*60 and timeDiff > 60:
            prefix = "{} hours ago".format(round(timeDiff / 60))
        elif timeDiff < 31 * 24 * 60 and timeDiff > 24 * 60:
            prefix = "{} days ago".format(round(timeDiff / (60 * 24)))
        else:
            prefix = str(self.timestamp)

        return prefix

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

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


class File(models.Model):
    attachment = models.FileField(blank=True,null=True,
        upload_to='attachment',storage=FileSystemStorage())

    def __str__(self):
        return self.attachment.url