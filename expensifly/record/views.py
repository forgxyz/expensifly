from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from datetime import date
from django_pandas.io import read_frame

from .models import Expense, ExpenseForm

# change selected_date
def set_month(request, year=date.today().year, month=date.today().month):
    # only load for this user id 
    request.session['selected_date'] = date(year, month, 1)

    transactions_month = Expense.objects.filter(date__year=request.session['selected_date'].year).filter(date__month=request.session['selected_date'].month)
    request.session['transaction_list'] = transactions_month
    request.session['total_month'] = transactions_month.aggregate(Sum('amount'))['amount__sum']

    request.session['total_year'] = Expense.objects.filter(date__year=request.session['selected_date'].year).aggregate(Sum('amount'))['amount__sum']

    tx = read_frame(transactions_month, fieldnames=['category', 'amount'])
    request.session['top_cats'] = tx.groupby('category').sum().sort_values('amount', ascending=False).to_dict()

    return HttpResponseRedirect(reverse('record:index'))


# load main overview screen. if first load, gather months from db and set SELECTED_DATE to current month
def index(request):
    if request.user.is_authenticated:
        if not request.session.get('initialize', False):
            request.session['initialize'] = True
            request.session['months'] = Expense.objects.dates('date', 'month').order_by('-datefield')
            set_month(request)
        return render(request, 'record/index.html')
    return HttpResponseRedirect(reverse('record:login'))


# load Expense ModelForm
def record(request):
    context = {'form': ExpenseForm()}
    return render(request, 'record/record.html', context=context)

# handle Expense ModelForm submission
def save(request):
    # save new transaction information to database
    if request.method == 'POST':
        # expense submission
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # save the input
            amount = form.cleaned_data['amount']
            sel_date = form.cleaned_data['date']
            category = form.cleaned_data['category']
            method = form.cleaned_data['method']
            comment = form.cleaned_data['comment']
            tag = form.cleaned_data['tag']

            e = Expense.objects.create(amount=amount, date=sel_date, category=category, method=method, comment=comment, tag=tag)

            # if new month - add to nav
            if date(sel_date.year, sel_date.month, 1) not in request.session['months']:
                request.session['months'] = Expense.objects.dates('date', 'month').order_by('-datefield')

        return HttpResponseRedirect(reverse('record:index'))

    # if not POST, redirect to form load
    return HttpResponseRedirect(reverse('record:record'))

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.

# load list of transactions
def transactions(request):
    context = {}
    return render(request, 'record/tx_list.html', context=context)


# log user in
def ulogin(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # context = {'message': f'Welcome, {request.user}', 'message_type': 'success'}
            return HttpResponseRedirect(reverse('record:index'))
        context = {'message': 'Unable to log in.', 'message_type': 'warning'}
        return render(request, 'record/login.html', context=context)

    # otherwise load login screen
    return render(request, 'record/login.html')


def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('record:login'))
