from django.core.management.base import BaseCommand, CommandError
from career.models import Company


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("company_names", nargs="*")
        parser.add_argument("--all")
    
    def handle(self, *args, **options):

        if options["all"]:
            Company.objects.all().delete()
        else:
            for company in options["company_names"]:
                if Company.objects.filter(name=company).count() == 0:
                    self.stderr.write(f"{company} matching query does not exist.\n")
                else:
                    Company.objects.filter(name=company).delete()
