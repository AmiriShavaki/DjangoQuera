from django.core.management.base import BaseCommand, CommandError
from career.models import Company

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
def is_valid_email(value):
	try:
		validate_email(value)
	except ValidationError:
		return False
	else:
		return True

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("company_name", nargs=1)
        
        parser.add_argument("--name")
        parser.add_argument("--email")
        parser.add_argument("--phone")
        parser.add_argument("--description")
    
    def handle(self, *args, **options):
        
        if Company.objects.filter(name=options["company_name"][0]).count() == 0:
            raise CommandError("Company matching query does not exist.")

        for field in ("name", "email", "phone"):
            if options[field] == "":
                raise CommandError("{} cannot be blank.".format(field.title()))

        if options["name"] and len(options["name"]) > 50:
            raise CommandError("Error: Ensure this value has at most 50 characters (it has {}).".format(
                len(options["name"])                    
            ))
        
        c = Company.objects.get(name=options["company_name"][0])

        if options["name"] and Company.objects.filter(name=options["name"]).count():
            raise CommandError("Error: That name is already taken.")
        elif options["name"]:
            c.name = options["name"]

        if options["email"] and not is_valid_email(options["email"]):
            raise CommandError("Error: Enter a valid email address.")
        elif options["email"]:
            c.email = options["email"]

        phone = options["phone"]
        if phone and not (
			len(phone)==11 and phone[:2]=="09" or 
			len(phone)==13 and phone[:3]=="+98" or 
			len(phone)==14 and phone[:4]=="0098"
		):
            raise CommandError("Error: Phone number format is not valid.")
        elif options["phone"]:
            c.phone = options["phone"]

        if options["description"] and len(options["description"]):
            c.description = options["description"]
        
        c.save()      