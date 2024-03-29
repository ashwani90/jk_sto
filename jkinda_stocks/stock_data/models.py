from django.db import models

# Create your models here.

class Company(models.Model):
    code = models.CharField()
    name = models.CharField()
    group = models.CharField()
    sc_type = models.CharField()
    stock_index_type = models.IntegerField(null=True)
    disabled = models.BooleanField(default=False)
    symbol = models.CharField(default='')

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
    
class Dashboard(models.Model):
    name = models.CharField()
    description = models.TextField()
    title = models.CharField()
    enabled = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    
class Chart(models.Model):
    name = models.CharField()
    title = models.CharField()
    type = models.CharField(default="Line")
    content = models.JSONField(default=None)
    size = models.IntegerField(null=True)
    order = models.IntegerField()
    dashboard_id = models.ForeignKey(Dashboard, on_delete=models.DO_NOTHING)
    data = models.JSONField(null=True)
    deleted = models.BooleanField(default=False)