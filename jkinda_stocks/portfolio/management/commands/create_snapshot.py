# create snapshot of returns 
# if stock added update that and update other things as well
# save to snapshot table
# this table will be used in generating graphs for the portfolios

from django.core.management.base import BaseCommand, CommandError
from portfolio.models import Portfolio, PortfolioSnapshot
from datetime import datetime, date, timedelta

class Command(BaseCommand):
    help = "Save portfolio snapshot"
    
    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        today = date.today()
        portfolios = Portfolio.objects.filter(active=True)
        records_to_create = []
        for portfolio in portfolios:
            type = portfolio.type
            invested = portfolio.invested
            returns = portfolio.returns
            created = portfolio.created
            
            data = {
                "type": type,
                "invested": invested,
                "returns": returns,
                "created": created
            }
            records_to_create.append(PortfolioSnapshot(portfolio=portfolio, snapshot=data,date=today))
        PortfolioSnapshot.objects.bulk_create(records_to_create)
        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )