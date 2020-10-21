from django.db.models import Sum
from django_pandas.io import read_frame

from .models import Category, Expense
from .fusioncharts import *


def category_barchart(request):
    data_source = {
        "chart": {
            "caption": f"Top Categories For {request.session['selected_date'].year}",
            "theme": "fusion",
        },
        "data": []
    }

    # load data for chart
    transactions = fetch_transactions(request, request.session['selected_date'].year)

    for cat, amount in transactions['total_categories']['amount'].items():
        data = {'label': cat, 'value': int(amount)}
        data_source['data'].append(data)

    column2d = FusionCharts("bar2d", "categoryBarChart", "100%", "550", "categoryBarChart-container", "json", data_source)
    return column2d


def fetch_transactions(request, year, month=None, cat=None):

    # load tx for this user id
    transactions = Expense.objects.filter(user=request.user).filter(date__year=year)
    total_year = transactions.aggregate(Sum('amount'))['amount__sum']
    heading = ''

    # if request is for month, filter down further
    if month:
        heading = 'Month'
        transactions = transactions.filter(date__month=month)

    # filter again if category supplied
    if cat:
        heading = cat
        cat_obj = Category.objects.get(category=cat)
        transactions = transactions.filter(category=cat_obj)

    # compute total of query
    total = transactions.aggregate(Sum('amount'))['amount__sum']

    # compute total of categories
    total_categories = read_frame(transactions, fieldnames=['category', 'amount']).groupby('category').sum().sort_values('amount', ascending=False).to_dict()

    context = {'transactions': transactions, 'total': total, 'total_categories': total_categories, 'total_year': total_year, 'heading': heading}
    return context
