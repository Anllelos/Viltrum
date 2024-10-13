from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from .models import *
from .form import ChatMessageCreateForm

def chat_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all().order_by('-created')[:10]
    chat_messages = list(chat_messages)
    chat_messages.reverse()
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        other_user = next((member for member in chat_group.members.all() if member != request.user), None)

    if request.method == "POST":
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            data_context = {'message': message, 'user': request.user}
            return render(request, 'chat.html', data_context)

    data_context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name
    }

    return render(request, 'chat.html', data_context)

def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    try:
        other_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("El usuario no existe")

    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None
    # Buscar chatroom existente
    for chatroom in my_chatrooms:
        if other_user in chatroom.members.all():
            break
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)
