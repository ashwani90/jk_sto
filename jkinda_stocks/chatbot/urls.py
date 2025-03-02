from django.urls import path
from .views import get_chats, send_message

urlpatterns = [
    path("", get_chats, name="chat"),
    path("send/", send_message, name="send_message"),
    # path("forgot_password", views.forgot_password, name="forgot_password"),
    # path("reset_password", views.reset_password, name="reset_password"),
]
