from django.db import models
from django.contrib.auth.models import User
from stock_data.models import Company


class Portfolio(models.Model):
    TYPES =( 
        ("1", "Demo"), 
        ("2", "Main"), 
        ("3", "Planned"), 
        ("4", "Past"), 
        ("5", "Track"), 
    ) 
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField()
    description = models.CharField()
    stocks = models.ManyToManyField(Company, through="PortfolioStock",
        through_fields=("portfolio", "company"),)
    type = models.CharField(max_length=3, choices=TYPES)
    invested = models.CharField(default='0')
    returns = models.CharField(default='0')
    created = models.DateTimeField(null=True)
    last_updated = models.DateTimeField(null=True)
    active = models.BooleanField(default=True, null=True)


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    invested = models.CharField()
    current = models.CharField()
    shares = models.IntegerField(null=True)
    bought_at = models.FloatField(null=True)
    date_bought = models.DateTimeField()
    date_released = models.DateTimeField(null=True)
    
class PortfolioSnapshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING)
    snapshot = models.JSONField()
    date = models.DateField()