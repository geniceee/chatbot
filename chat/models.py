from django.contrib.auth import get_user_model
from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
User = get_user_model()

# class Document(models.Model):
#     # docfile = models.FileField(upload_to='documents/')
#     name = models.CharField(max_length=50) 
#     docimage = models.ImageField(upload_to='images/')

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    # timestamp = models.DateField(blank=False, default=datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    timestamp = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact.user.username

class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)
    msg_file = models.FileField(blank=True,null=True,
        upload_to='profilepic',storage=FileSystemStorage())

    def __str__(self):
        return "{}".format(self.pk) 

    def most_recent_message(self):
        return self.messages.order_by('-timestamp').all()[0].content

    def other_participants(self):
        return list(map(str,self.participants.all()))

    # def other_participants(self, contact):
    #     return list(map(str,self.participants.exclude(contact)))
