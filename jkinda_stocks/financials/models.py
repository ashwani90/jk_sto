from django.db import models
from stock_data.models import Company

# Create your models here.
TYPES =( 
        ("1", "Annual"), 
        ("2", "Quarter"), 
    ) 

class FinancialDocs(models.Model):
    company_name = models.CharField(default=None)
    # company = models.ForeignKey(Company, on_delete=models.DO_NOTHING,default=None)
    symbol = models.CharField(default=None)
    data = models.JSONField()
    date = models.DateField()
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=3, choices=TYPES)
    
class Financial(models.Model):
    # company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    symbol = models.CharField(default=None)
    data = models.JSONField()
    date = models.DateField()
    # will decide if we can show the data
    status = models.BooleanField() 
