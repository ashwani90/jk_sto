from django.core.management.base import BaseCommand, CommandError
from financials.models import FinancialDocs, Financial

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
    help = "Download and save financial docs"
    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }

    #Curl headers
    curl_headers = ''' -H "authority: beta.nseindia.com" -H "cache-control: max-age=0" -H "dnt: 1" -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36" -H "sec-fetch-user: ?1" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" -H "sec-fetch-site: none" -H "sec-fetch-mode: navigate" -H "accept-encoding: gzip, deflate, br" -H "accept-language: en-US,en;q=0.9,hi;q=0.8" --compressed'''


    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # Query the financial docs table and then find recently update companies
        # refresh recently added companies
        self.get_data_and_save("Annual")

        self.stdout.write(
            self.style.SUCCESS("Successfully Save the data ")
        )
        
    def get_data_and_save(self,period_d):
        symbol = "TATAMOTORS"
        URL = nsefetch("https://www.nseindia.com/api/results-comparision?symbol=TATAMOTORS")
        Financial.objects.create(symbol=symbol, data=URL, date=date.today(), status=1)
