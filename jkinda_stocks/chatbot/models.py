from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    content = models.TextField()
    response_to = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True)
    
    