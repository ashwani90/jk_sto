from django.core.management.base import BaseCommand, CommandError
from stock_data.models import Company, CompanyDetails
from financials.models import Financial

class Command(BaseCommand):
    help = "Generate Company details"

    def add_arguments(self, parser):
        parser.add_argument("--id", nargs="+", type=str)
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        given_ids = False
        if options['id']:
            company_id = options["id"][0]
        if not company_id:
            return
        if company_id == "All":
            company_ids = Company.objects.filter(stock_index_type__in=[0,1,2], disabled=False)
            
        else:
            given_ids = True
            company_ids = company_id.split(",")
        result_to_create = []
        for company in company_ids:
            if given_ids:
                company = Company.objects.get(id=company)
            try:
                financial = Financial.objects.filter(symbol=company.symbol).order_by('-date')[0]
                data = financial.data
                
                data = data.get("resultsData2")
                p_e = data.get("re_basic_eps")
                if not p_e:
                    continue
                revenue = data.get("re_net_sale")
                face_value = data.get("re_face_val")
                
                
                result_to_create.append(CompanyDetails(p_e=p_e, face_value=face_value, market_cap=revenue,company=company, employees=None))
            except Exception as e:
                print(e)
        CompanyDetails.objects.bulk_create(result_to_create)
        self.stdout.write(
            self.style.SUCCESS("Successfully Saved the data ")
        )