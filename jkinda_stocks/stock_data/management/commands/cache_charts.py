from django.core.management.base import BaseCommand, CommandError
from stock_data.models import Chart, Dashboard, Company

import urllib.request as urllib2
import json
import requests

from datetime import datetime, date, timedelta
import xml.etree.ElementTree as ET
from nsepython import *
import os,sys
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pandas as pd
import random
import re
import urllib.parse
import xmltodict
from stock_data.helpers import single_company_chart, multiple_company_chart, get_short_financials

class Command(BaseCommand):
    help = "cache dashboard charts for showing in dashboards"

    def add_arguments(self, parser):
        parser.add_argument("--ids", nargs="+", type=str)
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        chart_ids = False
        if options['ids']:
            chart_ids = options["ids"][0]
        # Query the chart need to be cached
        if chart_ids:
            chart_ids = chart_ids.split(",")
            charts = Chart.objects.filter(dashboard_id__enabled=True, id__in=chart_ids)
        else:
            charts = Chart.objects.filter(dashboard_id__enabled=True)
        result = False
        for chart in charts:
            print(chart.type)
            if chart.type == '1':
                result = self.create_company_chart(chart)
                
            if chart.type == '2':
                result = self.get_financial_company(chart)
            if result:
                Chart.objects.filter(id=chart.id).update(content=result)
            self.stdout.write(
                self.style.SUCCESS("Successfully Saved the data for chart")
            )
        # get data for all the charts

        self.stdout.write(
            self.style.SUCCESS("Successfully Saved the data ")
        )
    def create_company_chart(self, chart):
        chart_data = chart.data
        range = chart_data.get("range")
        company = chart_data.get("company")
        
        companies = company.split(",")
        if len(companies)>1:
            result = multiple_company_chart(companies, range)
        else:
            result = single_company_chart(company, range)
        return result
    
    def get_financial_company(self, chart):
        company = chart.data.get("company")
        symbol = Company.objects.filter(code=company,disabled=False)[0]
        return get_short_financials(symbol.symbol)