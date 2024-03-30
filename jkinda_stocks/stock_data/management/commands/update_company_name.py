from django.core.management.base import BaseCommand, CommandError
from stock_data.models import Company
from financials.models import Financial
from newsdata.models import NewsData
import csv
from fuzzywuzzy import process
import spacy
nlp = spacy.load("en_core_web_sm")

class Command(BaseCommand):
    help = "Update Company Name "
    
    def add_arguments(self, parser):
        parser.add_argument("--operation", nargs="+", type=str)
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        operation = False
        if options['operation']:
            operation = options["operation"][0]
        if operation == 'csv-write':
            results = Financial.objects.raw('SELECT 1 as id, symbol FROM financials_financial GROUP BY symbol')
            data = []
            for result in results:
                obj = Financial.objects.filter(symbol=result.symbol).order_by('-date').order_by('-id')[0]
                longname = obj.data.get('longname')
                print(longname)
                if longname:
                    data.append([longname, result.symbol])
            file_paths = "jkinda_stocks_data/data/"
            with open(file_paths+'file.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
                    # Company.objects.filter(symbol=result.symbol).update(name=longname)
                self.stdout.write(
                    self.style.SUCCESS('Processed id: "%s" ' % result.symbol)
                )
        else:
            # check similarity between company name and news
            news_data = NewsData.objects.filter(data__isnull=False)
            for news in news_data:
                self.process_news_data(news)
                self.stdout.write(
                    self.style.SUCCESS('Processed id: "%s" ' % news.id)
                )
            
    def process_news_data(self, news_data):
        
        tags = news_data.tags
        all_companies = self.read_csv_file()
        doc = nlp(tags)
        company_list = []
        for ent in doc.ents:
            
            if str(ent.label_) == "ORG":
                lists = process.extract(str(ent.text), all_companies)
                company_list = company_list + [li[0] for li in lists if li[1]>90]
        if len(company_list)>0:
            symbols = self.get_company_symbol(company_list)
            symbols = ",".join(symbols)
            print(symbols)
            NewsData.objects.filter(id=news_data.id).update(comp_symbols=symbols)
            
    def get_company_symbol(self, company_list):
        file_paths = "jkinda_stocks_data/data/"
        all_companies = []
        with open(file_paths+"/file.csv", mode ='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                all_companies.append([lines[0],lines[1]])
        comp_list = []
        for comp in all_companies:
            if comp[0] in company_list:
                comp_list.append(comp[1])
        return comp_list
            
    def read_csv_file(self):
        file_paths = "jkinda_stocks_data/data/"
        all_companies = []
        with open(file_paths+"/file.csv", mode ='r') as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                all_companies.append(lines[0])
        return all_companies