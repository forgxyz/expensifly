from django.db.models import Sum
from django_pandas.io import read_frame

from .models import Category, Expense, Income
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

    for cat, amount in transactions['expense_categories']['amount'].items():
        data = {'label': cat, 'value': int(amount)}
        data_source['data'].append(data)

    bar2d = FusionCharts("bar2d", "categoryBarChart", "90%", "550", "categoryBarChart-container", "json", data_source)
    return bar2d


def fetch_income(request, year, month=None):
    income = Income.objects.filter(user=request.user).filter(date__year=year)
    total_year = income.aggregate(Sum('amount'))['amount__sum']

    if month:
        income = income.filter(date__month=month)

    total = income.aggregate(Sum('amount'))['amount__sum']

    context = {'income_year': total_year, 'income_total_period': total}
    return context


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

    context = {'transactions': transactions, 'expense_total_period': total, 'expense_categories': total_categories, 'expense_year': total_year, 'heading': heading}
    return context


def weekly_expense(request, year, month=None):
    tx = fetch_transactions(request, year, month)

    df = read_frame(tx['transactions'], fieldnames=['date', 'amount'])

    # clean
    df['date'] = df['date'].astype('datetime64')
    df['amount'] = df['amount'].astype('float')

    # flatten expenses down into day
    df = df.groupby('date').sum()

    # add weekday column
    df['weekday'] = df.index.day_name()

    weekday_avg = df.groupby('weekday').mean().to_dict()

    # reconfigure to normal order
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_ordered = {}

    # set day to 0 in case no data
    for day in order:
        weekday_ordered[day] = weekday_avg['amount'].get(day, 0)

    data_source = {
    "chart": {
        "caption": "Average by Weekday",
        "theme": "fusion",
            },
        "data": []
        }

    for day, amount in weekday_ordered.items():
        data = {'label': day, 'value': int(amount)}
        data_source['data'].append(data)

    column2d = FusionCharts("column2d", "weekdayBarChart", "90%", "300", "weekdayBarChart-container", "json", data_source)

    return column2d
