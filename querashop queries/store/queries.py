from store.models import *
from django.db.models import Avg, Sum, Count, F
import datetime
from datetime import timedelta
from django.db import connection
from django.db.models.lookups import Exact

def young_employees(job: str):
    return Employee.objects.filter(job=job, age__lt=30)


def cheap_products():
    avg = Product.objects.aggregate(Avg("price"))
    res = Product.objects.filter(price__lt=avg["price__avg"]).order_by("price")
    return [item.name for item in res]


def products_sold_by_companies():
    qs = Company.objects.annotate(sold=Sum("product__sold"))
    names = [company.name for company in Company.objects.all()]
    return [(obj.name, obj.sold) for obj in qs]

def sum_of_income(start_date: str, end_date: str):
    from datetime import datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    return Order.objects.filter(time__gte=start_date, time__lte=end_date).aggregate(res=Sum("price"))["res"]


def good_customers():
    now = datetime.datetime.now()
    qs = Order.objects.filter(time__gte=now - timedelta(365/12))
    golds = Customer.objects.filter(level='G')
    res = [(customer.name, customer.phone) for customer in golds if qs.aggregate(res=Count("id", filter=Exact(F("customer__id"), customer.id)))["res"]>10]
    return res

def nonprofitable_companies():
    qs = Product.objects.filter(sold__lt=100)
    res = [company.name for company in Company.objects.all().iterator() if qs.aggregate(res=Count("id", filter=Exact(F("company__id"), company.id)))["res"]>=4]
    return res
