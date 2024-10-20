from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:username>', views.get_or_create_chatroom, name='start_chat'),
    path('chat/room/<str:chatroom_name>', views.chat_view, name='chatroom'),
    path('chat/', views.chats_list, name='chats_list'),  
]
