from django.http import JsonResponse
from .models import Dashboard
import os
import csv
from django.core.serializers import serialize
import datetime
import json
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.core import serializers
from financials.models import Financial
from newsdata.models import NewsData
from .helpers import get_date_range_from_range

def get_dashboards(request, search):
    dashboards = Dashboard.objects.filter(name__icontains=search)[:10]
    data = []
    for i in dashboards:
        data.append({"name": i.name, "id": i.id})
    
    return JsonResponse({"dashboards": data, "success": True})

