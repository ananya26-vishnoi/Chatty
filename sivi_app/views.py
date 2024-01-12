from django.shortcuts import render, redirect
from .models import *
import os
from rest_framework import status
from rest_framework.response import Response
from dotenv import load_dotenv 
load_dotenv()
import json
import random
import string
from rest_framework.decorators import api_view
from django.core.mail import send_mail

class UserFunctions:
    def index(request):
        try:
            # Checking if private key is present or not
            if not 'sivi_privatekey' in request.session:
                return redirect('login')
            
            # Checking if user exists or not
            private_key = request.session['sivi_privatekey']
            if User.objects.filter(private_key=private_key).exists():
                user = User.objects.get(private_key=private_key)
                name = user.username
                first_name = name.split(" ")[0]
                last_name = name.split(" ")[0][-1]
                if len(name.split(" ")) > 1:
                    last_name = name.split(" ")[1][0]
                name_abbr = first_name[0] + last_name
                name_abbr = name_abbr.upper()
                return render(request, 'chat.html', {'user': user, 'name_abbr': name_abbr})
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            return render(request, 'login.html')

    def login(request):
        return render(request, 'login.html')

    def signup(request):
        return render(request, 'signup.html')

    def logout(request):
        del request.session['sivi_privatekey']
        return redirect('login')

    def login_user(request):
        try:
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(email=email, password=password).exists():
                user = User.objects.get(email=email, password=password)
                private_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                request.session['sivi_privatekey'] = private_key
                user.private_key = private_key
                user.save()
                return redirect('index')
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            return redirect('login')
        
    def signup_user(request):
        try:
            email = request.POST['email']
            password = request.POST['password']
            username = request.POST['name']
            
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                
                if user.otp_verified :
                    return redirect('login')
                else:
                    otp = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                    user.otp = otp
                    user.save()
                    subject = "OTP for Sivi Project"
                    message = "Your OTP is "+str(otp) + "\n Please do not share with anyone else. \n\n Thanks, \n Ananya Vishnoi"
                    reciever_list = [email]
                    send_mail(subject,message,os.getenv('EMAIL_HOST_USER'),reciever_list)
                    return render(request, 'otp.html', {'email': email})
                
            # unique username
            elif User.objects.filter(username=username).exists():
                return redirect('signup')
            
            else:
                otp = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                user = User(email=email, password=password, username=username, otp = otp)
                user.save()
                subject = "OTP for Sivi Project"
                message = "Your OTP is "+str(otp) + "\n Please do not share with anyone else. \n\n Thanks, \n Ananya Vishnoi"
                reciever_list = [email]
                send_mail(subject,message,os.getenv('EMAIL_HOST_USER'),reciever_list)
                return render(request, 'otp.html', {'email': email})
        except Exception as e:
            print(e)
            return redirect('signup')
    
    def verify_otp(request):
        try:
            email = request.POST['email']
            otp = request.POST['otp']
            if User.objects.filter(email=email, otp=otp).exists():
                user = User.objects.get(email=email, otp=otp)
                user.otp_verified = True
                user.otp = ''
                user.save()
                return redirect('login')
            else:
                return render(request, 'otp.html', {'email': email})
        except Exception as e:
            print(e)
            return render(request, 'otp.html', {'email': email})

class Chat:
    @api_view(['POST'])
    def get_connections(request):
        try:
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                connection_list = json.loads(str(user.connections))
                final_list = []
                for x in connection_list:
                    temp_user = User.objects.get(id=x)
                    temp_dict = {
                        'id': temp_user.id,
                        'username': temp_user.username,
                        'email': temp_user.email,
                        'is_online': temp_user.is_online,
                    }
                    final_list.append(temp_dict)
                return Response({'connections': final_list}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['GET'])
    def chat_history(request):
        try:
            sender_email = request.GET['sender_email']
            reciever_id = request.GET['reciever_id']
            if User.objects.filter(email=sender_email).exists() and User.objects.filter(id=reciever_id).exists():
                sender = User.objects.get(email=sender_email)
                reciever = User.objects.get(id=reciever_id)
                chat_history = ChatHistory.objects.filter(sender=sender, receiver=reciever).order_by('created_at') | ChatHistory.objects.filter(sender=reciever, receiver=sender).order_by('created_at')
                final_list = []
                for x in chat_history:
                    sender_first_name = x.sender.username.split(" ")[0]
                    sender_last_name = x.sender.username.split(" ")[0][-1]
                    if len(x.sender.username.split(" ")) > 1:
                        sender_last_name = x.sender.username.split(" ")[1][0]
                    sender_name_short = sender_first_name[0] + "" + sender_last_name
                    sender_name_short = sender_name_short.upper()
                    print(sender_name_short)
                    temp_dict = {
                        'chat': x.chat,
                        'sender': x.sender.username,
                        'receiver': x.receiver.username,
                        'sender_id' : x.sender.id,
                        'created_at': x.created_at,
                        'sender_name_short' : sender_name_short ,
                    }
                    final_list.append(temp_dict)
                return Response({'chat_history': final_list,'reciever_name' : reciever.username}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @api_view(['POST'])
    def start_new_chat(request):
        try:
            sender_email = request.POST['sender_email']
            reciever_email = request.POST['reciever_email']
            if User.objects.filter(email=sender_email).exists() and User.objects.filter(email=reciever_email).exists():
                sender = User.objects.get(email=sender_email)
                reciever = User.objects.get(email=reciever_email)
                sender_connections = json.loads(str(sender.connections))
                reciever_connections = json.loads(str(reciever.connections))
                if reciever.id in sender_connections and sender.id in reciever_connections:
                    reciever_name = reciever.username
                    reciever_id = reciever.id
                    return Response({'message': 'Chat already started','reciever_name':reciever_name,'reciever_id':reciever_id}, status=status.HTTP_200_OK)
                
                if not reciever.id in sender_connections:
                    sender_connections.append(reciever.id)
                    sender.connections = json.dumps(sender_connections)
                    sender.save()
                if not sender.id in reciever_connections:
                    reciever_connections.append(sender.id)
                    reciever.connections = json.dumps(reciever_connections)
                    reciever.save()
                reciever_name = reciever.username
                reciever_id = reciever.id
                return Response({'message': 'Chat started','reciever_name':reciever_name,'reciever_id':reciever_id}, status=status.HTTP_200_OK) 
            else:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)