from django.db import models 
class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    private_key = models.CharField(max_length=100)
    otp = models.CharField(max_length=100)
    otp_verified = models.BooleanField(default=False)
    connections = models.JSONField(default=list,null=True,blank=True)
    socket_code = models.CharField(max_length=100)


class ChatHistory(models.Model):
    chat = models.CharField(max_length=1000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    
