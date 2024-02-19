from django.db import models

# Create your models here.

class NewsData(models.Model):
    date = models.DateField()
    data = models.TextField()
    processed = models.BooleanField(default=False)
    
