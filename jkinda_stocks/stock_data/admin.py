from django.contrib import admin

# Register your models here.
from .models import Company, Operators

admin.site.register(Company)
admin.site.register(Operators)