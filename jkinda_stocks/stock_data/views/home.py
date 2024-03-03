from django.shortcuts import render
from django.http import JsonResponse
from stock_data.apps.models import BSEStockData, NSEStockData, MCXStockData, NSEFOStockData, Company
import os
import csv
from django.core.serializers import serialize
import datetime
import json
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from financials.models import Financial

# Create your views here.

def compare_view(request):
    template = loader.get_template('pages/compare_view.html')
    return HttpResponse(template.render())

def update_company(request):
    unique_companies_id = []
    query = "select company_id_id, count(company_id_id) as company_count from stock_data_bsestockdata group by company_id_id order by company_count desc;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    for i in rows:
        unique_companies_id.append(i[0])
    company_id_string = ','.join(str(v) for v in unique_companies_id)
    return JsonResponse({'data': company_id_string})

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def company(request):
    company_data = Financial.objects.filter(symbol="TATAMOTORS")[0]
    template = loader.get_template('pages/company.html')
    return HttpResponse(template.render(), {company_data: company_data})

def show_data(request):
    code = request.GET.getlist("code")[0]
    company_data = Company.objects.filter(code=code,stock_index_type=0)
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
        result.append({"open": da.open, "close": da.close, "date": da.date_show})
    data = {"data": result, "companyDetails": company_details}
    # serialized_data = json.loads(serialized_data)
    return JsonResponse(data, safe=False)

def company_dropdown(request):
    try:
        name = request.GET.getlist("name")[0]
    except Exception as e:
        name = False
    if name:
        company_data = Company.objects.filter(stock_index_type=0,name__icontains=name).order_by('-id')[:100]
    else:
        company_data = Company.objects.filter(stock_index_type=0).order_by('-id')[:100]
    result = []
    for ca in company_data:
        result.append({"name": ca.name, "code": ca.code, 'group': ca.group})
    
    data = {"data": result}
    # serialized_data = json.loads(serialized_data)
    return JsonResponse(data, safe=False)

def save_data(request):
    # read file
    ab = []
    file_paths = "jkinda_stocks_data/data/"
    dirs = os.listdir(file_paths)
    jiter = 1
    for i in dirs:
        file_list = os.listdir(file_paths+i)
        for j in file_list:
            jiter = jiter + 1
            ab.append(file_paths+i+"/"+j)
            file_name = j.split('.')[0]
            if len(file_name) < 1:
                continue
            file_name = file_name.split("_")
            
            file_type = file_name[1]
            date_date = file_name[0]
            
            if file_type == "BSE":
                model_name = BSEStockData
            
                with open(file_paths+i+"/"+j, mode ='r') as file:
                    csvFile = csv.reader(file)
                    for lines in csvFile:
                        if len(lines) < 14:
                            continue
                        if lines[0] == 'SC_CODE':
                            continue
                        Company.objects.update_or_create(code=lines[0], name=lines[1], group=lines[2], sc_type=lines[3])
                        company = Company.objects.filter(code=lines[0])
                        if len(company) > 0:
                            company = company[0]
                        else:
                            company = company
                        day = int(date_date[6:8])
                        month = int(date_date[4:6])
                        year = int(date_date[0:4])
                        d = datetime.datetime(year, month, day)
                        try:
                            model_name.objects.update_or_create(open=lines[4], high=lines[5], low=lines[6],
                                                        close=lines[7], last=lines[8], prevclose=lines[9],
                                                        no_trades=lines[10], no_shrs=lines[11], net_turnov=lines[12],
                                                        td_clo_indi=lines[13], date_show=d, company_id=company)
                        except Exception as e:
                            print(e)
                            
    return JsonResponse({"a":ab})
    

def save_data2(request):
    # read file
    ab = []
    file_paths = "jkinda_stocks_data/data/"
    dirs = os.listdir(file_paths)
    jiter = 1
    for i in dirs:
        file_list = os.listdir(file_paths+i)
        for j in file_list:
            jiter = jiter + 1
            ab.append(file_paths+i+"/"+j)
            file_name = j.split('.')[0]
            if len(file_name) < 1:
                continue
            file_name = file_name.split("_")
            
            file_type = file_name[1]
            date_date = file_name[0]
            
            if file_type == "BSE":
                model_name = BSEStockData
                continue
            if file_type == "NSE":
                model_name = NSEStockData
                with open(file_paths+i+"/"+j, mode ='r') as file:
                    csvFile = csv.reader(file)
                    for lines in csvFile:
                        if len(lines) < 13:
                            continue
                        if lines[0] == 'SYMBOL':
                            continue
                        Company.objects.update_or_create(code=lines[0], name=lines[0], group=lines[1], sc_type=lines[1])
                        company = Company.objects.filter(code=lines[0])
                        if len(company) > 0:
                            company = company[0]
                        else:
                            company = company
                        day = int(date_date[6:8])
                        month = int(date_date[4:6])
                        year = int(date_date[0:4])
                        d = datetime.datetime(year, month, day)
                        try:
                            model_name.objects.update_or_create(open=lines[2], high=lines[3], low=lines[4],
                                                        close=lines[5], last=lines[6], prevclose=lines[7],
                                                        no_trades=lines[7], no_shrs=lines[8], net_turnov=lines[9],
                                                        td_clo_indi=lines[11], date_show=d, company_id=company)
                        except Exception as e:
                            print(e)
                            
                    continue
            if file_type == "MCX":
                model_name = MCXStockData
                continue
            if file_type == "NSEFO":
                model_name = NSEFOStockData
                continue
    return JsonResponse({"a":ab})

def save_data3(request):
    # read file
    ab = []
    file_paths = "jkinda_stocks_data/data2/"
    dirs = os.listdir(file_paths)
    jiter = 1
    for i in dirs:
        file_list = os.listdir(file_paths+i)
        for j in file_list:
            jiter = jiter + 1
            ab.append(file_paths+i+"/"+j)
            file_name = j.split('.')[0]
            if len(file_name) < 1:
                continue
            file_name = file_name.split("_")
            
            file_type = file_name[1]
            date_date = file_name[0]
            
            if file_type == "BSE":
                model_name = BSEStockData
            
                with open(file_paths+i+"/"+j, mode ='r') as file:
                    csvFile = csv.reader(file)
                    for lines in csvFile:
                        if len(lines) < 14:
                            continue
                        if lines[0] == 'SC_CODE':
                            continue
                        Company.objects.update_or_create(code=lines[0], name=lines[1], group=lines[2], sc_type=lines[3])
                        company = Company.objects.filter(code=lines[0])
                        if len(company) > 0:
                            company = company[0]
                        else:
                            company = company
                        day = int(date_date[6:8])
                        month = int(date_date[4:6])
                        year = int(date_date[0:4])
                        d = datetime.datetime(year, month, day)
                        try:
                            model_name.objects.update_or_create(open=lines[4], high=lines[5], low=lines[6],
                                                        close=lines[7], last=lines[8], prevclose=lines[9],
                                                        no_trades=lines[10], no_shrs=lines[11], net_turnov=lines[12],
                                                        td_clo_indi=lines[13], date_show=d, company_id=company)
                        except Exception as e:
                            print(e)
                            
    return JsonResponse({"a":ab})
    
def save_data4(request):
    # read file
    ab = []
    file_paths = "jkinda_stocks_data/data2/"
    dirs = os.listdir(file_paths)
    jiter = 1
    for i in dirs:
        file_list = os.listdir(file_paths+i)
        for j in file_list:
            jiter = jiter + 1
            ab.append(file_paths+i+"/"+j)
            file_name = j.split('.')[0]
            if len(file_name) < 1:
                continue
            file_name = file_name.split("_")
            
            file_type = file_name[1]
            date_date = file_name[0]
            
            if file_type == "BSE":
                model_name = BSEStockData
                continue
            if file_type == "NSE":
                model_name = NSEStockData
                with open(file_paths+i+"/"+j, mode ='r') as file:
                    csvFile = csv.reader(file)
                    for lines in csvFile:
                        if len(lines) < 13:
                            continue
                        if lines[0] == 'SYMBOL':
                            continue
                        Company.objects.update_or_create(code=lines[0], name=lines[0], group=lines[1], sc_type=lines[1])
                        company = Company.objects.filter(code=lines[0])
                        if len(company) > 0:
                            company = company[0]
                        else:
                            company = company
                        day = int(date_date[6:8])
                        month = int(date_date[4:6])
                        year = int(date_date[0:4])
                        d = datetime.datetime(year, month, day)
                        try:
                            model_name.objects.update_or_create(open=lines[2], high=lines[3], low=lines[4],
                                                        close=lines[5], last=lines[6], prevclose=lines[7],
                                                        no_trades=lines[7], no_shrs=lines[8], net_turnov=lines[9],
                                                        td_clo_indi=lines[11], date_show=d, company_id=company)
                        except Exception as e:
                            print(e)
                    continue
            if file_type == "MCX":
                model_name = MCXStockData
                continue
            if file_type == "NSEFO":
                model_name = NSEFOStockData
                continue
    return JsonResponse({"a":ab})