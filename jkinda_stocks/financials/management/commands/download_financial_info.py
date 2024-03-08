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
        parser.add_argument("--start_date", nargs="+", type=str)
        parser.add_argument("--end_date", nargs="+", type=str)
        parser.add_argument("--ids", nargs="+", type=str)

    def handle(self, *args, **options):
        # Query the financial docs table and then find recently update companies
        # refresh recently added companies
        company_ids = False
        today = date.today()
        formatted_date = today.strftime('%d-%m-%Y')
        yesterday = today - timedelta(1)
        yesterday = yesterday.strftime('%d-%m-%Y')
        
        records_to_create = []
        if options['ids']:
            company_ids = options["ids"][0]
            
        if options['start_date']:
            today = today - timedelta(options["start_date"])
            
        if options['end_date']:
            yesterday = today - timedelta(options["end_date"])
            yesterday = yesterday.strftime('%d-%m-%Y')
        today = formatted_date
        if company_ids:
            company_ids = company_ids.split(",")
            financial_docs = FinancialDocs.objects.filter(id__in=company_ids)
        else:
            financial_docs = FinancialDocs.objects.filter(status=False,date__range=[today,yesterday])[:200]
        for i in financial_docs:
            data = i.data
            if data.get("audited") != "Audited":
                FinancialDocs.objects.filter(id = i.id).update(status = True)
                continue
            params = data.get("params")
            seq_id = data.get("seqNumber")
            oldNewFlag = data.get("oldNewFlag")
            if not oldNewFlag:
                oldNewFlag = ''
            ind = data.get("reInd")
            format_ = data.get("format")
            try:
                URL = nsefetch("https://www.nseindia.com/api/corporates-financial-results-data?index=equities&params="+params+"&seq_id="+seq_id+"&industry=-&frOldNewFlag="+oldNewFlag+"&ind="+ind+"&format="+format_)
                records_to_create.append(Financial(symbol=i.symbol, data=URL, date=date.today(), status=False, type=1))
            except Exception as e:
                print(i.id)
                print(e)
            FinancialDocs.objects.filter(id = i.id).update(status = True)
        
        Financial.objects.bulk_create(records_to_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
        
# shareholding pattern later on
# complaints for investors
# We can also check debt data for particular companies
