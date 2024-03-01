from django.core.management.base import BaseCommand, CommandError
from financials.models import Events, FinancialDocs, Financial

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
    help = "Get company financials using financial docs"
    
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
        financial_docs = FinancialDocs.objects.filter(date=date.today(), status=False)
        records_to_create = []
        
        for i in financial_docs:
            data = i.data
            if data.get("audited") != "Audited":
                FinancialDocs.objects.filter(id = i.id).update(status = True)
                continue
            params = data.get("params")
            seq_id = data.get("seqNumber")
            oldNewFlag = data.get("oldNewFlag")
            ind = data.get("reInd")
            format_ = data.get("format")
            
            URL = nsefetch("https://www.nseindia.com/api/corporates-financial-results-data?index=equities&params="+params+"&seq_id="+seq_id+"&industry=-&frOldNewFlag="+oldNewFlag+"&ind="+ind+"&format="+format_)
            records_to_create.append(Financial(symbol=i.symbol, data=URL, date=date.today(), status=False, type=1))
            FinancialDocs.objects.filter(id = i.id).update(status = True)
        
        Financial.objects.bulk_create(records_to_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
        
# shareholding pattern later on
# complaints for investors
# We can also check debt data for particular companies
