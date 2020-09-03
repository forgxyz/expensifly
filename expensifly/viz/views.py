import pandas as pd

from datetime import date
from django.shortcuts import render
from django.db.models import Sum

from record.models import Expense


# default view will be a dashboard of spending of current month
def index(request, year=date.today().year, month=date.today().month):
    selected_date = date(year, month, 1)

    tx_year = Expense.objects.filter(date__year=year)
    tx_month = tx_year.filter(date__month=month)

    total_year, total_month = tx_year.aggregate(Sum('amount')), tx_month.aggregate(Sum('amount'))
    totals = {'year': format(round(total_year['amount__sum'],2), ',.2f'), 'month': format(round(total_month['amount__sum'], 2), ',.2f')}

    months = Expense.objects.dates('date', 'month')

    context = {"selected_date": selected_date, "tx": tx_month, "totals": totals, 'months': months}
    return render(request, 'viz/index.html', context=context)
