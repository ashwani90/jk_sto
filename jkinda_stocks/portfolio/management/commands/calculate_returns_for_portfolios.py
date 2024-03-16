from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Portfolio, PortfolioSnapshot, PortfolioStock
from datetime import datetime, date, timedelta
from stock_data.models import BSEStockData, NSEStockData

class Command(BaseCommand):
    help = "Save portfolio snapshot"
    
    def add_arguments(self, parser):
        parser.add_argument("--day", nargs="+", type=str)
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        today = date.today()
        day = 1
        if options['day']:
            day = int(options["day"][0])
        yesterday = today - timedelta(day)
        yesterday = yesterday.strftime('%Y-%m-%d')
        today = yesterday
        portfolios = Portfolio.objects.filter(active=True)
        stocks_bse_to_update = []
        stocks_nse_to_update = []
        bse_companies = []
        nse_companies = []
        for portfolio in portfolios:
            stocks = PortfolioStock.objects.filter(portfolio=portfolio, date_released__isnull=True).select_related('company')
            
            for stock in stocks:
                # get all the stocks
                # get current rate for the company
                # calculate current value
                shares = stock.shares
                company_id = stock.company.id
                stock_index = stock.company.stock_index_type
                if stock_index == 0:
                    stocks_bse_to_update.append({
                        'stock_id': stock.id,
                        'shares': shares,
                        "company": company_id,
                        "index": stock_index
                    })
                    bse_companies.append(company_id)
                else:
                    stocks_nse_to_update.append({
                        'stock_id': stock.id,
                        'shares': shares,
                        "company": company_id,
                        "index": stock_index
                    })
                    nse_companies.append(company_id)
                # get most recent stock price
        bse_stocks = BSEStockData.objects.filter(company_id_id__in=bse_companies, date_show=today)
        nse_stocks = NSEStockData.objects.filter(company_id_id__in=nse_companies, date_show=today)
        bse_dict = self.convert_to_dict(bse_stocks)
        nse_dict = self.convert_to_dict(nse_stocks)
        try:
            self.update_stock(stocks_bse_to_update, bse_dict)
            self.update_stock(stocks_nse_to_update, nse_dict)
        except Exception as e:
            print(e)
        # now update the value in portfolio
        for portfolio in portfolios:
            stocks = PortfolioStock.objects.filter(portfolio=portfolio, date_released__isnull=True)
            current_sum = 0
            for stock in stocks:
                current_sum = current_sum + float(stock.current)
            Portfolio.objects.filter(id=portfolio.id).update(returns=current_sum)
        
        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
    def convert_to_dict(self, stocks_):
        result = {}
        for stock in stocks_:
            if stock.company_id_id not in result:
                result[stock.company_id_id] = stock.close
        return result
    
    def update_stock(self, stocks_to_update, dictt):
        for stock in stocks_to_update:
            value = int(stock.get('shares'))*float(dictt[stock.get('company')])
            PortfolioStock.objects.filter(id=stock.get('stock_id')).update(current=value)