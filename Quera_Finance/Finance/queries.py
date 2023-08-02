from django.db.models import F, Sum, Count, Case, When, IntegerField
from .models import *


def query_0():
    q = Employee.objects.all()
    return q


def query_1():
    return Payslip.objects.filter(payment=None).aggregate(
        total_dept=Sum(F("base")+F("tax")+F("insurance")+F("overtime"))
    )


def query_2(x):
    return Payslip.objects.filter(
        salary__overtime__gte=x
    ).aggregate(total_overtime=Sum("overtime"))


def query_3():
    return Payment.objects.aggregate(total=Sum("amount"))


def query_4(x):
    if EmployeeProjectRelation.objects.filter(employee__id=x).count():
        return EmployeeProjectRelation.objects.filter(employee__id=x).aggregate(
            total_hours=Sum("hours")
        )
    return {"total_hours": None}


def query_5(x):
    return Employee.objects.annotate(total_paid_salary=Sum("salary__payslip__payment__amount")).filter(
        total_paid_salary__gt=x
    )

def query_6():
    qs = Employee.objects.annotate(total_hours=Sum("employeeprojectrelation__hours"))
    return qs.order_by("-total_hours", "account__username").first()


def query_7():
    return Department.objects.annotate(total=Sum("employee__salary__payslip__payment__amount")).order_by(
        "-total", "name"
    ).first()


def query_8():
    return Department.objects.annotate(res=Count(Case(
        When(project__end_time__lte=F("project__estimated_end_time"), then=1), output_field=IntegerField()
    ))).order_by("-res", "name").first()


def query_9(x):
    return Employee.objects.annotate(late_cnt=Count(Case(
        When(attendance__in_time__gt=x, then=1),
        output_field=IntegerField(),
    ))).order_by(
        "-late_cnt", "account__username"
    ).first()


def query_10():
    return {"total": Employee.objects.filter(employeeprojectrelation=None).count()}
