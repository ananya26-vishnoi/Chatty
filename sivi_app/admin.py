from django.contrib import admin 
from .models import User
from .models import ChatHistory

admin.site.register(User)
admin.site.register(ChatHistory)
