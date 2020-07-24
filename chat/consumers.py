from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Chat, Contact
from .views import get_user_contact, get_current_chat, get_last_10_messages

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # messages = Message.last_10_messages()
        messages = get_last_10_messages(data['room_name'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = get_user_contact(data['from'])
        # author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            contact=author, 
            content=data['message'])

        current_chat = get_current_chat(data['room_name'])
        current_chat.messages.add(message)
        current_chat.save()

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message),
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.contact.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if self.user.is_authenticated: # also you can add more restrictions here
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        # self.accept()

    #Leave room group
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    # Send message to room group
    def send_chat_message(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Send message to WebSocket
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))