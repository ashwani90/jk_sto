from django.db import models

# Create your models here.

class Company(models.Model):
    code = models.CharField()
    name = models.CharField()
    group = models.CharField()
    sc_type = models.CharField()
    stock_index_type = models.IntegerField(null=True)

class BSEStockData(models.Model):
    open = models.CharField()
    high = models.CharField()
    low = models.CharField()
    close = models.CharField()
    last = models.CharField()
    prevclose = models.CharField()
    no_trades = models.CharField()
    no_shrs = models.CharField()
    net_turnov = models.CharField()
    td_clo_indi = models.CharField()
    date_show = models.DateField()
    company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    
    
class NSEStockData(models.Model):
    open = models.CharField()
    high = models.CharField()
    low = models.CharField()
    close = models.CharField()
    last = models.CharField()
    prevclose = models.CharField()
    no_trades = models.CharField()
    no_shrs = models.CharField()
    net_turnov = models.CharField()
    td_clo_indi = models.CharField()
    date_show = models.DateField()
    company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    
class MCXStockData(models.Model):
    open = models.CharField()
    high = models.CharField()
    low = models.CharField()
    close = models.CharField()
    last = models.CharField()
    prevclose = models.CharField()
    no_trades = models.CharField()
    no_shrs = models.CharField()
    net_turnov = models.CharField()
    td_clo_indi = models.CharField()
    date_show = models.DateField()
    company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    
class NSEFOStockData(models.Model):
    open = models.CharField()
    high = models.CharField()
    low = models.CharField()
    close = models.CharField()
    last = models.CharField()
    prevclose = models.CharField()
    no_trades = models.CharField()
    no_shrs = models.CharField()
    net_turnov = models.CharField()
    td_clo_indi = models.CharField()
    date_show = models.DateField()
    company_id = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    