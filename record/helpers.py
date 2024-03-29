import pandas as pd

from django.db.models import Sum
from django_pandas.io import read_frame

from .models import Category, Expense, Income
from .fusioncharts import *


def category_chart(request):
    data_source = {
        "chart": {
            "centerlabel": "$label: $value",
            "decimals": 0,
            "numberPrefix": "$",
            "plottooltext": "$percentvalue",
            "showLabels": 0,
            "showValues": 0,
            "theme": "fusion",
        },
        "data": []
    }

    # load data for chart
    transactions = fetch_transactions(request, request.session['selected_date'].year)

    for cat, amount in transactions['expense_categories']['amount'].items():
        data = {'label': cat, 'value': int(amount)}
        data_source['data'].append(data)

    chart = FusionCharts("doughnut2d", "categoryChart", "100%", "600", "categoryChart-container", "json", data_source)
    return chart


def current_month_area(request):
    expense = fetch_transactions(request, request.session['selected_date'].year, request.session['selected_date'].month)
    income = fetch_income(request, request.session['selected_date'].year, request.session['selected_date'].month)

    expense_df = read_frame(expense['transactions'], fieldnames=['date', 'amount'])
    income_df = read_frame(income['income_tx'], fieldnames=['date', 'amount'])

    # clean
    expense_df['date'] = expense_df['date'].astype('datetime64[s]')
    expense_df['amount'] = expense_df['amount'].astype('float')
    expense_df['amount'] = expense_df['amount'] * -1

    income_df['date'] = income_df['date'].astype('datetime64[s]')
    income_df['amount'] = income_df['amount'].astype('float')

    df = pd.concat([expense_df, income_df])

    # flatten expenses down into day
    df = df.groupby('date').sum()

    cumsum = df.cumsum().to_dict()['amount']

    data_source = {
    "chart": {
        "theme": "fusion",
        "numberPrefix": "$",
        "xaxisname": "Day of Month",
        "yaxisname": "Net $$$$"
            },
        "data": []
    }

    for date, amount in cumsum.items():
        data = {'label': str(date.date().day), 'value': amount}
        data_source['data'].append(data)

    chart = FusionCharts("area2d", "cumsumChart", "100%", "400", "cumsumChart-container", "json", data_source)

    return chart


def fetch_income(request, year, month=None):
    income = Income.objects.filter(user=request.user).filter(date__year=year)
    total_year = income.aggregate(Sum('amount'))['amount__sum']

    if month:
        income = income.filter(date__month=month)

    total = income.aggregate(Sum('amount'))['amount__sum']

    context = {'income_year': total_year, 'income_total_period': total, 'income_tx': income}
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
    df['date'] = df['date'].astype('datetime64[s]')
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
        "theme": "fusion",
            },
        "data": []
    }

    for day, amount in weekday_ordered.items():
        data = {'label': day, 'value': int(amount)}
        data_source['data'].append(data)

    chart = FusionCharts("column2d", "weekdayBarChart", "100%", "400", "weekdayBarChart-container", "json", data_source)

    return chart

def budget_adherence(request, year, month=None):
    tx = fetch_transactions(request, year, month)

    df = read_frame(tx['transactions'], fieldnames=['date', 'amount', 'budgeted'])

    # clean
    df['date'] = df['date'].astype('datetime64[s]')
    df['amount'] = df['amount'].astype('float')
    df['budgeted'] = df['budgeted'].astype('bool')

    # sum expenses by category
    df = df.groupby('budgeted')['amount'].sum()

    context = df.to_dict()

    return context
