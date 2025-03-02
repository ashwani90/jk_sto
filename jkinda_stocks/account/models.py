from django.db import models
from django.contrib.auth.models import User


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    
class Organization(models.Model):
    name = models.CharField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return  self.name
    
class Role(models.Model):
    name = models.CharField()
    description = models.TextField()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None)
    delHistoryDate = models.DateTimeField(blank=True, null=True, default=None)
    token = models.CharField(default=None, blank=True, null=True, max_length=255)
    chat_token = models.CharField(default=None, blank=True, null=True)
