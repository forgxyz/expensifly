import pandas as pd

from datetime import date
from django.shortcuts import render
from django.db.models import Sum

from record.models import Expense


# default view will be a dashboard of spending
def index(request, year=date.today().year, month=date.today().month):
    # default to current month
    tx_year = Expense.objects.all().filter(date__year=year)
    tx_month = tx_year.filter(date__month=month)

    total = tx_year.aggregate(Sum('amount'))
    total_month = tx_month.aggregate(Sum('amount'))

    months = Expense.objects.dates('date', 'month')

    context = {"selected_month": month, "tx": tx_month, "total": total, "total_month": total_month, 'months': months}
    return render(request, 'viz/index.html', context=context)
