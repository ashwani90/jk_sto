from django.db import models

# Create your models here.

class NewsData(models.Model):
    date = models.DateField()
    data = models.TextField()
    processed = models.BooleanField(default=False)
    tags = models.CharField(default="", null=True)
    generic_nouns = models.TextField(default="", null=True)
    nouns_phrases = models.TextField(default="", null=True)
    comp_symbols = models.CharField(default="", null=True)