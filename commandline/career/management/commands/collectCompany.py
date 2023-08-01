from django.core.management.base import BaseCommand, CommandError
from career.models import Company

class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open("company.csv", 'w')
        for company in Company.objects.all().iterator():
            f.write(",".join((company.name, company.email, company.phone)) + '\n')
        f.close()