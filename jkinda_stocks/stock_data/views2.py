from django.shortcuts import render
from django.http import JsonResponse
from .models import BSEStockData, NSEStockData, MCXStockData, NSEFOStockData, Company, Dashboard, Chart, Operators
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
from django.contrib.auth.decorators import login_required
from account.models import User, Profile
from .query import create_query
import requests


# Create your views here.
@login_required
def compare_view(request):
    data = {}
    return render(request, 'pages/compare_view.html', data)

@login_required
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

@login_required
def index(request):
    dashboard_id = False
    try:
        dashboard_id = request.GET.get("dashboard_id")
    except Exception:
        pass
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    # get user
    chat_data = {}
    profile = Profile.objects.get(user=user)
    response = requests.get('http://localhost:8000/api/v1/get_user?username='+user.username+'&token='+profile.token)
    if response:
        response = json.loads(response.content)
        chat_user_id = response.get('user_id')
        room_id = response.get('room_id')
        chat_data = {
            'chat_user_id': chat_user_id,
            'room_id': room_id,
            'unique_token': profile.chat_token
        }
    if not dashboard_id:
        try:
            dashboard = Dashboard.objects.filter(user=user).order_by('-default')[0]
        except Exception as e:
            print(e)
            dashboard = []
            data = {"chart_data": [], "dashboards": [], "dash": [], 'chat_data': chat_data}
            return render(request, 'index.html', data)
    else:
        dashboard = Dashboard.objects.get(id=int(dashboard_id))
    charts = Chart.objects.filter(dashboard_id=dashboard, deleted=False)
    dashboards = Dashboard.objects.filter(enabled=True, user=user)
    current_dashboard = {
        "name": dashboard.name,
        "title": dashboard.title
    }
    all_dash = []
    for dashboard in dashboards:
        all_dash.append({
            "id": dashboard.id,
            "name": dashboard.name
        })
    chart_data = []
    for chart in charts:
        chart_data.append({
            "id": chart.id,
            "type": chart.type,
            "content": chart.content,
            "size": chart.size,
            "order": chart.order,
            "name": chart.name,
            "title": chart.title
        })
    data = {"chart_data": chart_data, "dashboards": all_dash, "dash": current_dashboard, 'chat_data': chat_data}
    return render(request, 'index.html', data)

def company_list(request):
    operator = request.GET.get("op")
    result = create_query(operator)
    data = {"result": result}
    return render(request, 'pages/company-list.html', data)

@login_required
def company(request):
    symbol="SANOFI"
    symbol = request.GET.get("symbol")
    company_data = Financial.objects.filter(symbol=symbol, type=1).order_by('-id')
    if company_data:
        company_data = company_data[0]
    else:
        data = {}
        return render(request, 'pages/company.html', data)
    operators = Operators.objects.all()
    operators_ar = []
    for operator in operators:
        operators_ar.append({
            "name": operator.name,
            "value": operator.value,
            "operators": operator.db_operator
        })
    data = company_data.data
    print(data)
    
    company_name = data.get("longname")
    data = data.get("resultsData2")
    total_revenue = data.get("re_total_inc")
    profit = data.get("re_pro_loss_bef_tax")
    face_value = data.get("re_face_val")
    equity_share = data.get("re_pdup")
    e_per_share = data.get("re_basic_eps")
    debt_equity = data.get("re_debt_eqt_rat")
    data = {
        "company_name": company_name,
        "total_revenue": total_revenue,
        "profit": profit,
        "face_value": face_value,
        "equity_share": equity_share,
        "e_per_share": e_per_share,
        "debt_equity": debt_equity,
        "symbol": symbol,
        "sector": "IT",
        "all_operators": operators_ar
    }
    print(data)
    return render(request, 'pages/company.html', data)


def get_companies(request, search):
    companies = Company.objects.filter(name__icontains=search, stock_index_type__in=[0,2], disabled=False)[:10]
    data = []
    for i in companies:
        data.append({"name": i.name, "id": i.code})
    
    return JsonResponse({"companies": data, "success": True})

@login_required
def get_messages(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    response = requests.get('http://localhost:8000/api/v1/get_messages?username='+user.username+'&token='+profile.token)
    if response:
        response = json.loads(response.content)
        messages = response.get('messages')
    return JsonResponse({"messages": messages, "success": True})

def get_short_financials(request, symbol):
    if not symbol:
        symbol = "SANOFI"
    company_data = Financial.objects.filter(symbol=symbol, type=1).order_by('-date')
    if company_data:
        company_data = company_data[0]
    else:
        data = {}
        return JsonResponse({"companies": data, "success": False})
    data = company_data.data
    
    company_name = data.get("longname")
    data = data.get("resultsData2")
    total_revenue = data.get("re_total_inc")
    profit = data.get("re_pro_loss_bef_tax")
    face_value = data.get("re_face_val")
    equity_share = data.get("re_pdup")
    e_per_share = data.get("re_basic_eps")
    debt_equity = data.get("re_debt_eqt_rat")
    data = {
        "company_name": company_name,
        "total_revenue": total_revenue,
        "profit": profit,
        "face_value": face_value,
        "equity_share": equity_share,
        "e_per_share": e_per_share,
        "debt_equity": debt_equity,
        "symbol": symbol,
        "sector": "IT"
    }
    return JsonResponse({"companies": data, "success": True})
    

def get_financials(request, symbol):
    # get request financials
    if not symbol:
        data = {}
        return JsonResponse({"message": "No Data", "success": False})
    company_data = Financial.objects.filter(symbol=symbol, type=1).order_by('-id')
    if company_data:
        company_data = company_data[0]
    else:
        data = {}
        return JsonResponse({"message": "No Data", "success": False})

    data = company_data.data
    data = data.get("resultsData2")
    revenue = data.get("re_net_sale")
    other_income = data.get("re_oth_inc_new")
    total_revenue = data.get("re_total_inc")
    material_consumed = data.get("re_rawmat_consump")
    material_consumed2 = data.get("re_pur_trd_goods")
    change_inventories = data.get("re_inc_dre_sttr")
    employee_benefit = data.get("re_staff_cost")
    finance_costs = data.get("re_int_new")
    depre_amor_expenses = data.get("re_depr_und_exp")
    other_expenses = data.get("re_oth_exp")
    profit = data.get("re_pro_bef_int_n_excep")
    exceptional_items = data.get("re_excepn_items_new")
    profit_before_tax = data.get("re_pro_loss_bef_tax")
    current_tax = data.get("re_curr_tax")
    defferred_tax = data.get("re_deff_tax")
    total_tax_expense = data.get("re_tax")
    profit_period = data.get("re_proloss_ord_act")
    associate_share = data.get("re_share_associate")
    consolidated_profit = data.get("re_con_pro_loss")
    comprehensive_income = data.get("re_com_ic")
    total_compr_income = data.get("re_tot_com_ic")
    profit_attributes = data.get("re_pl_own_par")
    total_profit_non_controlling = data.get("re_tot_pl_nci")
    comprehensive_income_parent = data.get("re_com_ic")
    total_compr_non_contr_interests = data.get("re_tot_com_ic")
    paid_up_equity_share = data.get("re_pdup")
    face_value = data.get("re_face_val")
    basic_eps = data.get("re_basic_eps_for_cont_dic_opr")
    diluted_eps = data.get("re_dilut_eps_for_cont_dic_opr")
    interest_service_coverage = data.get("re_int_ser_cov")
    data = {
        "revenue": revenue,
        "other_income": other_income,
        "total_revenue": total_revenue,
        "material_consumed": material_consumed,
        "material_consumed2": material_consumed2,
        "change_inventories": change_inventories,
        "employee_benefit": employee_benefit,
        "finance_costs": finance_costs,
        "depre_amor_expenses": depre_amor_expenses,
        "other_expenses": other_expenses,
        "profit": profit,
        "exceptional_items": exceptional_items,
        "profit_before_tax": profit_before_tax,
        "current_tax": current_tax,
        "defferred_tax": defferred_tax,
        "associate_share": associate_share,
        "total_tax_expense": total_tax_expense,
        "profit_period": profit_period,
        "consolidated_profit": consolidated_profit,
        "comprehensive_income": comprehensive_income,
        "total_compr_income": total_compr_income,
        "profit_attributes": profit_attributes,
        "total_profit_non_controlling": total_profit_non_controlling,
        "comprehensive_income_parent": comprehensive_income_parent,
        "total_compr_non_contr_interests": total_compr_non_contr_interests,
        "paid_up_equity_share": paid_up_equity_share,
        "face_value": face_value,
        "basic_eps": basic_eps,
        "diluted_eps": diluted_eps,
        "interest_service_coverage": interest_service_coverage
    }
    return JsonResponse({"financials": data, "success": True})
    
@login_required
def get_news(request):
    company_id = 1
    news = NewsData.objects.filter(company_id=company_id)
    newsList = []
    for i in news:
        newsList.append(i.data)
    return JsonResponse({news: newsList}, safe=False)
   

def show_data(request):
    code = request.GET.getlist("code")[0]
    codes = code.split(",")
    singleCode = False
    if len(codes) == 1:
        singleCode = True
    try:
        singleCode = request.GET.getlist("is_single")[0]
        if singleCode == '0':
            singleCode = False
    except Exception as e:
        print("Exception here")
    
    try:
        range = request.GET.getlist("range")[0]
    except Exception as e:
        range = 50
    singleCode = bool(singleCode)
    
    
    # Convert range into date range
    ranges = get_date_range_from_range(range)
    if singleCode:
        company_data = Company.objects.filter(code=code,stock_index_type__in=[0,2], disabled=False)
        if company_data and len(company_data) > 0:
            company_data = company_data[0]
        if not company_data:
            return JsonResponse({"success": False})
        company_name = company_data.name
        company_code = company_data.code
        company_details = {"name": company_name, 'code': company_code}
        if company_data.stock_index_type == 0:
            data = BSEStockData.objects.filter(company_id=company_data.id,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
        else:
            data = NSEStockData.objects.filter(company_id=company_data.id,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
        result = []
        for da in data:
            result.append({"open": da.open, "close": da.close, "low": da.low, "high": da.high, "date": da.date_show})
        data = {"data": result, "companyDetails": company_details}
        # serialized_data = json.loads(serialized_data)
        return JsonResponse(data, safe=False)
    else:
        company_data = Company.objects.filter(code__in=codes,stock_index_type__in=[0,2], disabled=False)
        if not company_data:
            return JsonResponse({"success": False})
        company_ids = []
        company_codes_map = {}
        for company in company_data:
            company_ids.append(company.id)
            company_codes_map[company.id] = company.code
        data = BSEStockData.objects.filter(company_id__in=company_ids,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
        result = {}
        for da in data:
            company_code = company_codes_map[da.company_id.id]
            if company_code not in result:
                result[company_code] = []
            result[company_code].append({"close": da.close, "high": da.high, "low": da.low, "open": da.open, "date": da.date_show})
        data = NSEStockData.objects.filter(company_id__in=company_ids,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
        for da in data:
            company_code = company_codes_map[da.company_id.id]
            if company_code not in result:
                result[company_code] = []
            result[company_code].append({"close": da.close, "high": da.high, "low": da.low, "open": da.open, "date": da.date_show})
        data = {"data": result}
        return JsonResponse(data, safe=False)
    
@login_required
def company_dropdown(request):
    try:
        name = request.GET.getlist("name")[0]
    except Exception as e:
        name = False
    if name:
        company_data = Company.objects.filter(stock_index_type__in=[0,2],name__icontains=name, disabled=False).order_by('-id')[:100]
    else:
        company_data = Company.objects.filter(stock_index_type__in=[0,2], disabled=False).order_by('-id')[:100]
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
                        # Company.object.filter(code=lines[0], stock_index_type=0)
                        # Company.objects.update_or_create(code=lines[0], name=lines[1], group=lines[2], sc_type=lines[3])
                        company = Company.objects.filter(code=lines[0], stock_index_type=0)
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
                        # Company.objects.update_or_create(code=lines[0], name=lines[0], group=lines[1], sc_type=lines[1])
                        company = Company.objects.filter(code=lines[0], stock_index_type__in=[1,2])
                        if not company:
                            continue
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
            if True:
            
                with open(file_paths+i+"/"+j, mode ='r') as file:
                    csvFile = csv.reader(file)
                    for lines in csvFile:
                        try:
                            Company.objects.filter(code=lines[1]).update(symbol=lines[3])
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