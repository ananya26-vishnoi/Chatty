from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserFunctions.index, name='index'),
    path('login', views.UserFunctions.login, name='login'),
    path('signup', views.UserFunctions.signup, name='signup'),
    path('logout', views.UserFunctions.logout, name='logout'),
    path('login_user', views.UserFunctions.login_user, name='login_user'),
    path('signup_user', views.UserFunctions.signup_user, name='signup_user'),
    path('verify_otp', views.UserFunctions.verify_otp, name='verify_otp'),

    path('getConnections', views.Chat.get_connections, name='getConnections'),
    path('chatHistory', views.Chat.chat_history, name='chatHistory'),
    path('startNewChat', views.Chat.start_new_chat, name='startNewChat'),
]
