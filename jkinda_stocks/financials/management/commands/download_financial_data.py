from django.core.management.base import BaseCommand, CommandError
from financials.models import FinancialDocs, Financial

import urllib.request as urllib2
import json
import requests

from datetime import date, timedelta
import xml.etree.ElementTree as ET
from nsepython import *
import os,sys
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(1, os.path.join(sys.path[0], '..'))

import pandas as pd
import random
import datetime,time
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
        
        # headers = {
        #     "authority": "www.nseindia.com",
        #     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        #     "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
        #     "cache-control": "max-age=0",
        #     "if-modified-since": "Sat, 17 Feb 2024 12:51:33 GMT",
        #     "if-none-match": "W/\"20809-1708174293000\"",
        #     "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        #     "sec-ch-ua-mobile": "?0",
        #     "sec-ch-ua-platform": "\"Linux\"",
        #     "sec-fetch-dest": "document",
        #     "sec-fetch-mode": "navigate",
        #     "sec-fetch-site": "none",
        #     "sec-fetch-user": "?1",
        #     "upgrade-insecure-requests": "1",
        #     "cookie": "_ga=GA1.1.105643382.1694346182; _ga_PJSKY6CFJH=GS1.1.1694352054.2.1.1694355100.60.0.0; _ga_QJZ4447QD3=GS1.1.1708244148.1.1.1708244793.0.0.0; _ga_87M7PJ3R97=GS1.1.1708244131.1.1.1708244793.0.0.0; ak_bmsc=BD4A270CD785562C1B2B390011F25671~000000000000000000000000000000~YAAQjs8uF6/ztIGNAQAAKr22uxZqib+n0STrpfwGk+OVxzVLFgSKMhXUIM1A1Bp8EpOQ4n4fZLxBW5rWsBTBOH7ZWR7VBO6327ZsR8yQ7Iy+6I3TtHoZyxWo6afJ8hv95K6hSG2Mwgwg6mgk802ZRhg7R+0j+ZRC/tMnDusZmjBodkoxd8NsoLg6wIRU3ErjuI8FKcKp3KFSWg12b/S8CdxaByJtqDjmbFzaH5e+DilxdidaLBz4VcFPEuxFvsYhiOc2vn6jR9m8Hs8tyXnbjJYP7wolZiCdVlG4sl4xhyABUoX5RgXDAzOrnRn07pby4nkgZzLOsjhPyX0V0JtRz/mdEWZk4tlkykKCmL0pevUgosYRgArJ/UwoRm5Dm09NTJ8kcX1aYtA/PePp; RT=\"z=1&dm=nseindia.com&si=22a13f3b-80c1-4748-ad3f-4779468670f9&ss=lsr8g6e8&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d48.akstat.io%2F\"; bm_sv=ACAB33D9B2E4260021C630C62FF7C429~YAAQjs8uF1wat4GNAQAAqKC+uxYrQoS1KDYL2o5FjTHRhQRTHl29aKLS1YGk1ZHBU3Fy36I2yZKstwCTn4aJq47XFHAzv2bvcQrCAVZZ5ve17rwMKW3kZ3v9Yp7znZoL5KET2JCJfjXSncAObmQBTacVUe4UyZ+UHKqnKJntxW5OjdhT/V+MQ6loHETY7PVUN1vO36gCFCGVdyR/6QWZW7cbt3w0eQfhRD0nWcrAchRxYruTm6GXpuU/KnrgBMD+wNokNw==~1",
        #     "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        #     }
        # page = requests.get(URL, headers=headers)
        # print(page.text)
        # print("Unable to get data")
        # tree = ET.fromstring(page.text)
        # root = tree.getroot() 
        # print(root)
        # find older record of this same company and mark status = 0
        Financial.objects.create(symbol=symbol, data=URL, date=date.today(), status=1)
        
        
    # def nsefetch2(self, payload):
    #     if (("%26" in payload) or ("%20" in payload)):
    #         encoded_url = payload
    #     else:
    #         encoded_url = urllib.parse.quote(payload, safe=':/?&=')
    #     payload_var = 'curl -b cookies.txt "' + encoded_url + '"' + self.curl_headers + ''
    #     try:
    #         output = os.popen(payload_var).read()
    #         print(output)
    #         output=xmltodict.parse(output)
    #     except ValueError:  # includes simplejson.decoder.JSONDecodeError:
    #         payload2 = "https://www.nseindia.com"
    #         output2 = os.popen('curl -c cookies.txt "'+payload2+'"'+self.curl_headers+'').read()
    
    #         output = os.popen(payload_var).read()
    #         # output=json.loads(output)
    #     return output