from django.core.management.base import BaseCommand, CommandError
from newsdata.models import NewsData

import urllib.request as urllib2
import json
import requests

import requests
from datetime import date, timedelta, datetime

from bs4 import BeautifulSoup
import pandas as pd
import arrow
import re

class Command(BaseCommand):
    help = "Download and save news"
    headers = {
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        
        try:
            
            r = requests.get('https://www.business-standard.com/', headers=self.headers)
        except:
            print("link invalid")
            pass
        print ('link accessed')
        soup = BeautifulSoup(r.text, "html.parser")
        all_as = soup.find_all('a')
        self.get_and_save_data_from_link(all_as)
        unique_as = set(self.get_urls(all_as))
        for un_as in unique_as:
            r = requests.get(un_as, headers=self.headers)
            soup = BeautifulSoup(r.text, "html.parser")
            all_as = soup.find_all('a')
            self.get_and_save_data_from_link(all_as)

        self.stdout.write(
                self.style.SUCCESS("Successfully Save the data ")
        )
        
    def get_urls(self, all_as):
        if not all_as:
            return []
        result_as = []
        for a in all_as:
            data = a.get('href')
            if not data:
                continue
            data = data.strip()
            if ('about' in data):
                continue
            if ('.html' in data):
                continue
            if 'today' in data:
                continue
            if '/market-statistics/' in data:
                continue
            if 'www.business-standard.com' not in data:
                continue
            if '.pdf' in data:
                continue
            data2 = data.split("/")
            if data2[-2] == 'www.business-standard.com' and data2[-1] == "":
                continue
            result_as.append(data)
        return result_as
    
    def get_and_save_data_from_link(self, all_as):
        records_to_create = []
        for a in all_as:
            data = a.get('href')
            
            if data and '.html' in data:
                html = requests.get(data, headers=self.headers)
                soup1 = BeautifulSoup(html.text, "html.parser")
                head = soup1.find_all('div', { "class" : "story-detail"})
                if head and head[0] and head[0].get_text():
                    if (self.check_if_insert(head[0].get_text())):
                        records_to_create.append(NewsData(data=head[0].get_text(), date=date.today(), processed=False))
        if len(records_to_create): 
            NewsData.objects.bulk_create(records_to_create)
            
    def check_if_insert(self, data):
        match_str = re.compile(r' \w{3} \d{2} \d{4} | ')
        match_str = match_str.findall(data)
        result = []
        for i in match_str:
            if i == " ":
                match_str.remove(" ")
                continue
            i = i.strip()
            result.append(i)
        if len(result) == 0:
            return False
        date_ = result[-1]
        date_obj = datetime.strptime(date_, '%b %d %Y')
        today = datetime.today()
        if today > date_obj:
            return True
        else:
            return True