from cabin.models import *
from django.db.models import Case, When, F, Count, Sum, IntegerField, FloatField, Q, Subquery, OuterRef
from django.db.models.lookups import GreaterThan, GreaterThanOrEqual
from django.db.models.functions import Cast

def query_0(x):
    q = Driver.objects.filter(rating__gt=x)
    return q


def query_1(x):
    value = Driver.objects.annotate(payment_sum=Sum("car__ride__payment__amount")).get(id=x).payment_sum
    return {'payment_sum': value}


def query_2(x):
    q = Ride.objects.filter(request__rider__id=x)
    return q


def query_3(t):
    q = Ride.objects.aggregate(res=Count('id', filter=GreaterThan(
        F("dropoff_time")-F("pickup_time"), t
    )))
    return q["res"]

def query_4(x, y, r):
    q = Driver.objects.filter(active=True).annotate(
        distance=Cast(( (F('x')-x)**2 + (F('y')-y)**2 )**.5, FloatField())
    ).filter(distance__lte=r)
    return q


def query_5(n, c):
    q = Driver.objects.annotate(ride_cnt=Count("car__ride")).filter(ride_cnt__gte=n).filter(
        Q(car__car_type='A') | Q(car__color=c)
    )
    return q


def query_6(x, t):
    q = Rider.objects.annotate(ride_cnt=Count("riderequest__ride")).filter(ride_cnt__gte=x)
    q = q.annotate(total_paid=Sum("riderequest__ride__payment__amount")).filter(total_paid__gt=t)
    return q


def query_7():
    subq = Subquery(Account.objects.filter(riders__riderequest__ride__car__owner__id=OuterRef("id")).
        values_list("first_name")
    )
    q = Driver.objects.filter(account__first_name__in=subq)
    return q


def query_8():
    q = ""
    return q


def query_9(n, t):
    q = Driver.objects.annotate(n=Count(F("car__ride__id"), filter=Q(GreaterThanOrEqual(F("car__model"), n))&Q(GreaterThan(F("car__ride__dropoff_time")-F("car__ride__pickup_time"), t))))
    return q.values("id", "n")


def query_10():
    q = Car.objects.annotate(extra=Case(
        When(car_type='A', then=Count("ride")),
        When(car_type='B', then=Sum(F("ride__dropoff_time")-F("ride__pickup_time"))),
        When(car_type='C' ,then=Sum(F("ride__payment__amount"))),
        output_field=IntegerField()
    ))
    return q
