from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import csv
from django.core.serializers import serialize
from stock_data.models import Dashboard, Chart, BSEStockData, Company
import datetime
import json
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_dashboard(request):
    print(request)
    if request.method == "POST":
        dash_name = request.POST.get('dash_name')
        print(dash_name)
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        member = Dashboard(name=dash_name, title=title, description=desc)
        member.save()
        return redirect(get_dashboards)
        # current_user_profile = request.user.profile
        # data = request.POST
        # action = data.get("follow")
        # if action == "follow":
        #     current_user_profile.follows.add(profile)
        # elif action == "unfollow":
        #     current_user_profile.follows.remove(profile)
        # current_user_profile.save()
    template = loader.get_template('pages/create_dashboard.html')
    return HttpResponse(template.render())

def get_dashboards(request):
    dashboards = Dashboard.objects.filter()[:100]
    return render(request,'pages/dashboards.html', {"dashboard_list": dashboards})

@csrf_exempt
def create_chart(request):
    if request.method == "POST":
        dash_id = request.POST.get('dashboard_id')
        chart_name = request.POST.get('chart_name')
        chart_type = request.POST.get('chart_type')
        chart_range = request.POST.get('chart_range')
        chart_company = request.POST.get('chart_company')
        chart_title = request.POST.get('chart_title')
        content = {
            "range": chart_range,
            "company": chart_company
        }
        company_data = Company.objects.filter(code=chart_company,stock_index_type=0)
        if company_data and len(company_data) > 0:
            company_data = company_data[0]
        if not company_data:
            return JsonResponse({"success": False})
        company_name = company_data.name
        company_code = company_data.code
        company_details = {"name": company_name, 'code': company_code}
        data = BSEStockData.objects.filter(company_id=company_data.id).order_by('-date_show')[:50]
        # serialized_data = serialize("json", data)
        result = []
        for da in data:
            result.append({"open": da.open, "close": da.close, "date": str(da.date_show)})
        data = {"data": result, "companyDetails": company_details}
        
        dashboard = Dashboard.objects.filter(id=dash_id).first()
        member = Chart(type=chart_type, size=0, order=1,name=chart_name,title=chart_title, dashboard_id=dashboard, content=content, data=data)
        member.save()
        return JsonResponse({"success": True})
    
def chart_preview(request, dashboard_id):
    dashboard = Dashboard.objects.filter(id=dashboard_id).first()
    charts = Chart.objects.filter(dashboard_id=dashboard)
    data = []
    
    for chart in charts:
        data.append(
            {
                "id": chart.id,
                "name": chart.name,
                "title": chart.title,
                "type": chart.type,
                "content": chart.content,
                "size": chart.size,
                "order": chart.order,
                "data": chart.data
            }
        )
    return render(request,'pages/dashboard_preview.html', {"dashboard": dashboard, "charts": data})

def get_chart_data(request):
    chart_ids = request.GET.get('chart_ids')
    
    charts = Chart.objects.filter(id__in=chart_ids)
    data = []
    for chart in charts:
        data.append({
            "data": chart.data
        })
    
    return JsonResponse({"success": True, "data": data})