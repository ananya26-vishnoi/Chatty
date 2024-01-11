import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random
import string
from .models import User, ChatHistory
from asgiref.sync import sync_to_async

@sync_to_async
def update_socket_code(email,socket_code):
    user = User.objects.get(email = email)
    user.socket_code = socket_code
    user.save()

@sync_to_async
def get_socket_code(reciever_id):
    user = User.objects.get(id = reciever_id)
    return user.socket_code

@sync_to_async
def add_to_history(message,reciever_id,email):
    sender = User.objects.get(email=email)
    receiver = User.objects.get(id =reciever_id )
    ChatHistory.objects.create(chat = message,sender = sender, receiver = receiver)

@sync_to_async
def get_short_name(email):
    user = User.objects.get(email=email)
    name = user.username
    first_name = name.split(" ")[0]
    last_name = name.split(" ")[0][-1]
    if len(name.split(" ")) > 1:
        last_name = name.split(" ")[1][0]
    name_abbr = first_name[0] + last_name
    name_abbr = name_abbr.upper()
    return name_abbr,user.id


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get("query_string", b"").decode("utf-8")
        email = query_string.split('=')[1]
        self.room_group_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        

        # Add user to the private chat group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await update_socket_code(email,self.room_group_name)
        
        print("accepted")
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the private chat group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Frontend Disconnected")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        reciever_id = text_data_json['reciever_id']
        email = text_data_json['email']

        # Send message to the receiver's private chat channel
        print(message,reciever_id,email)
        socket_code = await get_socket_code(reciever_id)
        await add_to_history(message,reciever_id,email)
        print(socket_code)
        # call a function to get socket id of the reciever and send a message on that after saving data in database
        await self.channel_layer.group_send(
            socket_code,{
                "type" : "sendMessage" ,
                "message" : message,
                "sender" : email
            })
        
    async def sendMessage(self , event) : 
        message = event["message"]
        email = event["sender"]
        
        short_name,chat_id = await get_short_name(email)
        await self.send(text_data = json.dumps({"message":message,"short_name":short_name,"chat_id":chat_id}))