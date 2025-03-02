from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Chat
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .helpers import get_reply

# Create your views here.
@login_required
def get_chats(request):
    
    return render(request, 'pages/chat.html')

@login_required
@csrf_exempt
def send_message(request):
    message = request.POST.get('message')
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # save the message
    
    chat = Chat.objects.create(user_id=user, content=message)
    # get a reply for the message
    reply = []
    reply = get_reply(message)
    Chat.objects.create(user_id=user, content=reply, response_to=chat)
    # later on reply will become asynchronous
    return JsonResponse({'reply': reply, "success": True})