from django.http import JsonResponse
from .models import Dashboard, Company, Chart
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
from django.views.decorators.csrf import csrf_exempt
from account.models import User

def get_dashboards(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    dashboards = Dashboard.objects.filter(user=user)[:20]
    data = []
    for i in dashboards:
        data.append({"name": i.name, "id": i.id})
    
    return JsonResponse({"dashboards": data, "success": True})

@csrf_exempt
def add_chart_to_dashboard(request):
    dash_id = request.POST.get('dashboard_id')
    company = request.POST.get('company')
    chart_data = request.POST.get('chartData')
    range = 50
    chart_data = json.loads(chart_data)
    if not chart_data.get('range'):
        chart_data["range"] = range
    company_codes = company
    company = company.split(",")[0]
    company = Company.objects.filter(code=company)[0]
    type = chart_data["type"]
    size = 1
    order = 0
    name = company.name
    title = company.name + " " + company.code
    data = {
        "range": chart_data["range"],
        "company": company_codes
    }
    dashboard = Dashboard.objects.filter(id=dash_id)[0]
    status = Chart.objects.create(name=name, type=type, size=size, order=order,
                                    title=title, data=data,dashboard_id=dashboard,content={})
    if status:
        return JsonResponse({"message": "Successfully added chart", "success": True})
    else:
        return JsonResponse({"message": "Unable to add chart", "success": True})