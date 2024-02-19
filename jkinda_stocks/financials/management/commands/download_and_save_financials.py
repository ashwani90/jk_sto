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
        yesterday = today + timedelta(-1)
        yesterday = yesterday.strftime('%d-%m-%Y')
        today = formatted_date
        
        json_data = nsefetch("https://www.nseindia.com/api/corporates-financial-results?index=equities&from_date="+yesterday+"&to_date="+today+"&period="+period_d)
        # print(URL)
        # headers = {'authority': 'www.nseindia.com', 
        #            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #            'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6' ,
        #             'cache-control': 'max-age=0' ,
        #             'cookie': '_ga=GA1.1.105643382.1694346182; _ga_PJSKY6CFJH=GS1.1.1694352054.2.1.1694355100.60.0.0; nsit=W6KAgEtAVzFt_qNp-VXAGTjS; defaultLang=en; ak_bmsc=593B5DB44D8F1EF01E2CC8E090224129~000000000000000000000000000000~YAAQjs8uF92AnIGNAQAAiehIuxbBdRZTfbXZLO+B6eY7Wld6V4ES0zCVkKcSkMiEBRidofSeaqtlTfdUry8/68OJ+6GZY6Uqs08oZ3l4q+yZ7KV0D2bBDlQbuoCMrqDY2fZ1D0gpPdpg2vU1YpxAzSUYgqeNTKrU57LvpUNLlaCYNKWUj5QyZRCryqNuFYKWt3mOIng52WDanx/uw1VCdnh8FOUelvSx1SvgFOo5cYA+cumeqKh8kUwqgUbsPF7yYy1T/pdlpj3gtzjyTxYERkOXFHJ6pgc9gkDv0MeURBZpzLMyVK652/3hUXWVQkvGwtcBxSv750ilZ2KRl0RHSBGR6kMaX2qGNIPrWBl3egUfYWNiks/7KCzPbpAV2e+KBFhIS5QcBEaIGmCp4GOLR5kNOKdFCdp5u9AjMzwcCx8jPuOaiMARKKd5AvyX/be6yIK5ccXFrkNT+Ffv6+LeDXWYI1R/onjaoLDdtAwHhjneOzX37UIlnoDr17V1AaZprg==; nseQuoteSymbols=[{"symbol":"WIPRO","identifier":null,"type":"equity"}]; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcwODI0NDQ3OSwiZXhwIjoxNzA4MjUxNjc5fQ.4cqbgx_qFwjVOgVKqfYVCwG_2BqI94WVkxfaPwwRxto; _ga_QJZ4447QD3=GS1.1.1708244148.1.1.1708244793.0.0.0; _ga_87M7PJ3R97=GS1.1.1708244131.1.1.1708244793.0.0.0; RT="z=1&dm=nseindia.com&si=22a13f3b-80c1-4748-ad3f-4779468670f9&ss=lsr8getk&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d4b.akstat.io%2F"; bm_sv=802210FE1FB2D675EFE9189DAB053A6A~YAAQjs8uF0rGqYGNAQAACuuEuxa4qWePaD6D37NWcMgQp5lmIx3/CggBa/KqpdQ9T8nNHzCRxqSevnKKR5MsacI2txwa1OOlluUlbl9XHWtQMN1mAtJL7qDTmqJ/VuNciuZeALxzDngk25QCExbDohvEQ/H8LUo7DHdY6psHpVeYyZEQUor3eIl6+Q1y4HKSXmxXcXh4n5cvQZve8U0cgvBng8Buxi3NepvwaLMsfNgtCCD2YrWA0YgKFvDdq/Sy4v4KjQ==~1' ,
        #             'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        #             'sec-ch-ua-mobile': '?0' ,
        #             'sec-ch-ua-platform': '"Linux"' ,
        #             'sec-fetch-dest': 'document' ,
        #             'sec-fetch-mode': 'navigate' ,
        #             'sec-fetch-site': 'none' ,
        #             'sec-fetch-user': '?1' ,
        #             'upgrade-insecure-requests': '1' ,
        #             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        #            }
        # page = requests.get(URL, headers=headers)
        # json_data = json.loads(page.text)
        
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
        