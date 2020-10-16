from collections import OrderedDict
from django.db.models import Sum
from django_pandas.io import read_frame

from .models import Expense
from .fusioncharts import *

def category_barchart(request):
    dataSource = {
        "chart": {
            "caption": f"Top Categories For {request.session['selected_date'].year}",
            "theme": "fusion",
        },
        "data": []
    }

    # load data for chart
    transactions = fetch_transactions(request, request.session['selected_date'].year)

    for cat, amount in transactions['total_categories']['amount'].items():
        data = {}
        data['label'] = cat
        data['value'] = int(amount)
        dataSource['data'].append(data)

    column2D = FusionCharts("bar2d", "categoryBarChart", "100%", "550", "categoryBarChart-container", "json", dataSource)
    return column2D


def fetch_transactions(request, year, month=None):

    # load tx for this user id
    transactions = Expense.objects.filter(user=request.user).filter(date__year=year)
    total_year = transactions.aggregate(Sum('amount'))['amount__sum']
    
    # if request is for month, filter down further
    if month:
        transactions = transactions.filter(date__month=month)

    # compute total of query
    total = transactions.aggregate(Sum('amount'))['amount__sum']

    # compute total of categories
    total_categories = read_frame(transactions, fieldnames=['category', 'amount']).groupby('category').sum().sort_values('amount', ascending=False).to_dict()

    context = {'transactions': transactions, 'total': total, 'total_categories': total_categories, 'total_year': total_year}
    return context
