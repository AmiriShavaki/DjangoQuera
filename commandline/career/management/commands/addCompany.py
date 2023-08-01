from django.core.management.base import BaseCommand
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
	def handle(self, *args, **options):
		name = input("Name: ")
		while True:
			if name == "":
				self.stderr.write("Error: This field cannot be blank.")
			elif len(name) > 50:
				self.stderr.write(
					f"Error: Ensure this value has at most 50 characters (it has {len(name)})."
				)		
			elif Company.objects.filter(name=name).count():
				self.stderr.write("Error: That name is already taken.")
			else:
				break
			name = input("Name: ")	
		
		email = input("Email: ")
		while True:
			if email == "":
				self.stderr.write("Error: This field cannot be blank.")
			elif not is_valid_email(email):
				self.stderr.write("Error: Enter a valid email address.")
			else:
				break
			email = input("Email: ")

		phone = input("Phone:")
		while True:
			if phone == "":
				self.stderr.write("Error: This field cannot be blank.")
			elif not (
				len(phone)==11 and phone[:2]=="09" or 
				len(phone)==13 and phone[:3]=="+98" or 
				len(phone)==14 and phone[:4]=="0098"
			):
				self.stderr.write("Error: Phone number format is not valid.")
			else:
				break
			phone = input("Phone:")

		description = input("Description:")
		if description == "":
			description = None

		Company.objects.create(name=name, email=email, phone=phone, description=description)