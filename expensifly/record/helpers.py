from django.db.models import Sum

from datetime import date

from .models import Expense


def get_spending(year=date.today().year, month=date.today().month):
    selected_date = date(year, month, 1)

    tx_year = Expense.objects.filter(date__year=year)
    tx_month = tx_year.filter(date__month=month)

    total_year, total_month = tx_year.aggregate(Sum('amount')), tx_month.aggregate(Sum('amount'))
    totals = {'year': format(round(total_year['amount__sum'],2), ',.2f'), 'month': format(round(total_month['amount__sum'], 2), ',.2f')}

    top_cats = tx_month.values('category__category').annotate(Sum('amount')).order_by('-amount')[:3]

    months = Expense.objects.dates('date', 'month')

    context = {"selected_date": selected_date, "tx": tx_month, "totals": totals, 'top_cats': top_cats, 'months': months}
    return context
