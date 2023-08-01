from django.db import models
from django_jalali.db import models as jmodels
import datetime
import jdatetime
from django.utils import timezone

class CustomUser(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    username = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    national_code = models.CharField(max_length=10)
    country = models.CharField(max_length=4, default="Iran")
    birthday_date = jmodels.jDateField()
    ceremony_datetime = jmodels.jDateTimeField()

    def get_first_and_last_name(self):
        first_name, last_name = self.full_name.split(' ')
        return {'first_name': first_name, 'last_name': last_name}
    
    def get_age(self):
        delta = datetime.datetime.today().date() - self.birthday_date
        return delta.days//365

    def is_birthday(self):
        bd = self.birthday_date
        today = jdatetime.date.fromgregorian(date=timezone.localtime(timezone.now()))
        return today.day == bd.day and today.month == bd.month