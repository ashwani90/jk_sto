from datetime import date, timedelta
from .models import Company, BSEStockData, NSEStockData
from financials.models import Financial

def get_date_range_from_range(range):
    today = date.today()
    prev_date = today
    range = int(range)
    if range == int(1):
        prev_date =  today - timedelta(days=7)
    if range == int(4):
        prev_date =  today - timedelta(days=30)
    if range == int(500):
        prev_date =  today - timedelta(days=(365*5))
    if range == int(50):
        prev_date =  today - timedelta(days=365)
    return [prev_date,today]

def single_company_chart(code, range):
    ranges = get_date_range_from_range(range)
    company_data = Company.objects.filter(code=code,stock_index_type__in=[0,2], disabled=False)
    if company_data and len(company_data) > 0:
        company_data = company_data[0]
    if not company_data:
        return []
    company_name = company_data.name
    company_code = company_data.code
    company_details = {"name": company_name, 'code': company_code}
    if company_data.stock_index_type == 0:
        data = BSEStockData.objects.filter(company_id=company_data.id,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
    else:
        data = NSEStockData.objects.filter(company_id=company_data.id,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
    result = []
    for da in data:
        result.append({"open": da.open, "high": da.high, "low": da.low, "close": da.close, "date": str(da.date_show)})
    return result, company_details

def multiple_company_chart(codes, range):
    ranges = get_date_range_from_range(range)
    company_data = Company.objects.filter(code__in=codes,stock_index_type__in=[0,2], disabled=False)
    if not company_data:
        return []
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
        result[company_code].append({"close": da.close, "high": da.high, "low": da.low, "open": da.open, "date": str(da.date_show)})
    data = NSEStockData.objects.filter(company_id__in=company_ids,date_show__range=(ranges[0], ranges[1])).order_by('-date_show')
    for da in data:
        company_code = company_codes_map[da.company_id.id]
        if company_code not in result:
            result[company_code] = []
        result[company_code].append({"close": da.close, "high": da.high, "low": da.low, "open": da.open, "date": str(da.date_show)})
    return result

def get_short_financials(symbol):
    if not symbol:
        symbol = "SANOFI"
    company_data = Financial.objects.filter(symbol=symbol, type=1).order_by('-date')
    if company_data:
        company_data = company_data[0]
    else:
        data = {}
        return data
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
    return data