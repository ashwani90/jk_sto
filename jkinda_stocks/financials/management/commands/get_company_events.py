from django.core.management.base import BaseCommand, CommandError
from financials.models import Events

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

class Command(BaseCommand):
    help = "Get Company Events"
    
    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # Query the financial docs table and then find recently update companies
        # refresh recently added companies
        today = date.today()
        formatted_date = today.strftime('%d-%m-%Y')
        yesterday = today + timedelta(-1)
        yesterday = yesterday.strftime('%d-%m-%Y')
        today = formatted_date
        symbol = "TATAMOTORS"
        URL = nsefetch("https://www.nseindia.com/api/event-calendar?index=equities&from_date="+yesterday+"&to_date="+today)
        records_to_create = []
        for i in URL:
            symbol = i.get('symbol')
            company = i.get('company')
            purpose = i.get('purpose')
            details = i.get('bm_desc')
            date_ = i.get('date')
            date_format = '%d-%b-%Y'
            date_obj = datetime.datetime.strptime(date_, date_format).date()
            records_to_create.append(Events(company=company, symbol=symbol, purpose=purpose, date=date_obj, details=details))
            
        Events.objects.bulk_create(records_to_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
        
# shareholding pattern later on
# complaints for investors
# We can also check debt data for particular companies
