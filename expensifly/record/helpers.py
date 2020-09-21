from django.db.models import Sum

from datetime import date

from .models import Expense


def get_spending(SELECTED_DATE):
    tx_year = Expense.objects.filter(date__year=SELECTED_DATE.year)
    tx_month = tx_year.filter(date__month=SELECTED_DATE.month)

    totals = {'year': tx_year.aggregate(Sum('amount'))['amount__sum'], 'month': tx_month.aggregate(Sum('amount'))['amount__sum']}

    top_cats = tx_month.values('category__category').annotate(Sum('amount'))

    context = {"tx": tx_month, "totals": totals, 'top_cats': top_cats}
    return context
