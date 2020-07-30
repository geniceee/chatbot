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
