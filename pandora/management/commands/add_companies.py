import os
import ijson
from django.core.management.base import BaseCommand
from django.db import transaction
from pandora.models import Company


class Command(BaseCommand):
    help = """Loads countries into database in Pandora Country Format"""

    def add_arguments(self, parser):
        parser.add_argument("--json_file", dest="json_file", help="Country JSON File")

    @transaction.atomic
    def handle(self, *args, **options):
        json_file_path = options.get("json_file")

        if not json_file_path:
            self.stdout.write(self.style.ERRROR("JSON File not Specified"))
            exit(0)

        try:
            os.stat(json_file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERRROR("JSON File doesnt Exist"))
            exit(0)

        companies_li = list()
        with open(json_file_path) as f:
            companies = ijson.items(f, "item")
            for company in companies:
                company_id = company.get("index") + 1
                name = company.get("company")
                company = Company(company_id=company_id, name=name)
                companies_li.append(company)

                if len(companies_li) > 500:
                    Company.objects.bulk_create(companies_li)
                    companies_li.clear()

        if companies_li:
            Company.objects.bulk_create(companies_li)
            companies_li.clear()
