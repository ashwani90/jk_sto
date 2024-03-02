from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .forms import PortfolioForm
from django.contrib.auth.decorators import login_required
from account.models import User
from .models import Portfolio, PortfolioStock
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from stock_data.models import Company
from datetime import datetime
from .utils import convert_tuple_to_list
# Create your views here.


# make a list of featured to be implemented
# create portfolio
# add / remove stock from portfolio
# update amount of shares for a stock
# management script to calculate returns on a stock
# delete a portfolio
# generate a graph for a portfolio 

@login_required
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            
            portfolio = form.save(commit=False)
            portfolio.user_id = user
            portfolio.save()
            # messages.success(request, _('Created the portfolio.'))
            return redirect('portfolio')
            # return render(request, 'portfolio/create_portfolio.html', {'form': form, 'message': message})
            
    else:
        form = PortfolioForm()
    return render(request, 'portfolio/create_portfolio.html', {'form': form})

@login_required
def get_portfolios(request):
    user_id = request.user.id
    
    portfolios = Portfolio.objects.filter(user_id=user_id, active=True)
    data = []
    types_dict = convert_tuple_to_list(Portfolio.TYPES)
    j = 0
    for i in portfolios:
        if j == 0:
            active = True
        else:
            active = False
        data.append({
            "name": i.name,
            "type": types_dict[i.type],
            "returns": i.returns,
            "invested": i.invested,
            "active": active,
            "id": i.id
        })
        j = j + 1
    
    return render(request, 'portfolio/index.html', {'portfolios': data})
    
@login_required
def get_stocks(request):
    portfolio_id = request.GET.get("portfolio_id")
    stocks = PortfolioStock.objects.filter(portfolio_id=portfolio_id)
    stocks_portfolio = []
    
    for i in stocks:
        stocks_portfolio.append({
            "company": i.company.name,
            "invested": i.invested,
            "current": i.current,
            "shares": i.shares,
            "bought_at": "{:.2f}".format(i.bought_at),
            "date_bought": i.date_bought,
            "date_released": str(i.date_released)
        })
    return JsonResponse({'stocks': stocks_portfolio, "success": True})

@csrf_exempt
def add_stock(request):
    if request.method == "POST":
        portfolio_id = request.POST.get("portfolio_id")
        company_id = request.POST.get("company_id")
        invested = request.POST.get("invested")
        shares = request.POST.get("shares")
        date_bought = request.POST.get("date_bought")
        bought_at = float(int(invested)/int(shares))
        current = invested
        portfolio = Portfolio.objects.get(id=portfolio_id)
        company = Company.objects.get(id=company_id)
        date_bought = datetime.strptime(date_bought, "%m/%d/%Y").date()
        
        try:
            stock = PortfolioStock(
                portfolio=portfolio,
                company=company,
                invested=invested,
                shares=shares,
                date_bought=date_bought,
                bought_at=bought_at,
                current=current
            )
            # TODO: if same share with different amount added perform addition of stock
            stock.save()
            return JsonResponse({'success': True, 'portfolio_id': portfolio_id})
        except Exception as e:
            # Todo log the exception maybe module wise
            print(e)
            return JsonResponse({'success': False})
        
        
@login_required
def update_portfolio(request):
    # update the stock base on action
    pass

@login_required
def delete_portfolio(request):
    # mark a portfolio inactive
    # the tracking of the portfolio will stop
    # TODO check if user is authorized to delete the portfolio
    user = request.user
    portfolio_id = request.GET.get("portfolio_id")
    status = Portfolio.objects.filter(id=portfolio_id).update(active=False)
    if status:
        return JsonResponse({'success': True, "message": "Deleted portfolio"})
    else:
        return JsonResponse({'success': False, "message": "Unable to delete portfolio"})

@login_required
def portfolio_graph(request):
    # can handle multiple portfolios
    # can accept date range
    # add to a dashboard feature
    # feature to check performance of portfolio if one/more stock is removed/added
    pass

@login_required
def list_famousPortfolios(request):
    # give a list of famous portfolios
    # once that is given clicking on one of that goes to dashboard view
    pass