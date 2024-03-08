from django.core.management.base import BaseCommand, CommandError
from financials.models import FinancialDocs

import urllib.request as urllib2
import json
import requests

import requests
from datetime import date, timedelta
from nsepython import *



class Command(BaseCommand):
    help = "Download and save financial docs"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        self.get_data_and_save("Quarterly")
        self.get_data_and_save("Annual")

        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
        
    def get_data_and_save(self,period_d):
        today = date.today()
        formatted_date = today.strftime('%d-%m-%Y')
        yesterday = today + timedelta(-365)
        yesterday = yesterday.strftime('%d-%m-%Y')
        today = formatted_date
        json_data = nsefetch("https://www.nseindia.com/api/corporates-financial-results?index=equities&from_date="+yesterday+"&to_date="+today+"&period="+period_d)
        
        records_to_create = []
        for i in json_data:
            symbol = i.get('symbol')
            company_name = i.get('companyName')
            period = i.get('period')
            if period == "Annual":
                type = 1
            else:
                type = 2
            records_to_create.append(FinancialDocs(company_name=company_name, symbol=symbol, data=i, date=date.today(), status=False, type=type))
        FinancialDocs.objects.bulk_create(records_to_create)