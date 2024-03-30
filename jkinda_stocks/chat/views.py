from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import ChatMessage,BotMsgToAll
from .forms import MessageForm
from itertools import chain
from operator import attrgetter
from django import forms
from django.http import JsonResponse
from botlogic.Lina.Lina import callBot,edit_real_time

@login_required
def index(request):
    
    #user and bot messages sent to the specific user
    chat_msgs_qs = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    #bot messages sent to all existing users
    bot_msgs_qs = BotMsgToAll.objects.filter(timestamp__gt=request.user.date_joined).order_by('timestamp')
    #joining the two list querysets into one sorted list queryset.
	#sorted by timestamp, can be sorted by -timestamp if 
	#reverse=True argument is added after key like in the api view
    result_list = sorted(chain(chat_msgs_qs,bot_msgs_qs),key=attrgetter('timestamp'))
    
    return render(request, "pages/chat.html", {
        "messages": result_list,
    })

@login_required
def message_to_all(request):
    if not (request.user.is_staff or  request.user.is_superuser):
        raise PermissionDenied   
    form = MessageForm(request.POST or None)
    if form.is_valid() and request.user.is_staff:
        instance = form.save(commit=False)
        instance.staff = request.user
        instance.save()
        messages.success(request, "Message Successfully Sent")
        return HttpResponseRedirect(reverse("broadcast"))
    title = 'send message'    
    return render(request,"registration/form.html",{"form":form,"title":title})

# not using websocket for now so just using the api calls

def chat_send(message):
    owner = "user"
    user = message.user #dont forget to check if user exist in DB 
    msg = message.GET.get('message')
    character = message.GET.get('character')
    field = forms.CharField()
    if not (field.clean(msg)):
        raise forms.ValidationError("Message can not be empty")
    msg = field.clean(msg)         
    # Save to model
    msg_obj = ChatMessage.objects.create(
        user = user,
        message = msg,
        owner = owner
    )
    if(msg_obj):
        final_msg = {
            "user":msg_obj.user.username,
            "msg": msg_obj.message,
            "owner": msg_obj.owner,
            "timestamp":msg_obj.formatted_timestamp
        }
    else:
        final_msg = {
            "user":user.username,
            "msg": "sorry ,DB error",
            "owner": owner,    
        }    
    response_type,response =callBot(msg,character)
    print(response)
    return JsonResponse({'stocks': final_msg, "success": True})
    #print("final_msg",final_msg)
    # Broadcast to listening socket(send user message to the user himself)
    # message.reply_channel.send({"text": json.dumps(final_msg)})

    #bot listening logic
    # payload = {
    #     'reply_channel': message.content['reply_channel'],
    #     'message': msg,
    #     'character':message.content['character'],
    # }
    # Channel("bot.receive").send(payload)