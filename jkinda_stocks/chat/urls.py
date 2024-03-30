
from .views import index,message_to_all, chat_send
from django.urls import path,include
from chat.api.views import index_api
from .api.views import (UserMessagesListAPIView,MessagesListAPIView,BroadcastMessageSendAPIView,
	UserMessagesDestroyAPIView)
urlpatterns = [
    path(r'chat/', index ,name='chat_index'),#home page
	path(r'chat/broadcast/', message_to_all, name='broadcast'),
    path(r'chat_send/', chat_send, name='chat_send'),
    path(r'chat/api/test/', index_api, name='jwt-test'),#for testing chat using jwt
    path(r'chat/api/messages/', UserMessagesListAPIView.as_view(),name='list'),
	path(r'chat/api/messages/delete', UserMessagesDestroyAPIView.as_view(),name='delete'),
	path(r'chat/api/messages/all', MessagesListAPIView.as_view(),name='list-all'),
	path(r'chat/api/messages/broadcast', BroadcastMessageSendAPIView.as_view(),name='broadcast'),
    
    # path("forgot_password", views.forgot_password, name="forgot_password"),
    # path("reset_password", views.reset_password, name="reset_password"),
]
