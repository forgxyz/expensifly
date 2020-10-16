from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datetime import date
from django_pandas.io import read_frame
from djmoney.money import Currency, Money
from djmoney.contrib.exchange.models import convert_money

from .models import Category, Expense, Income
from .forms import ExpenseForm, IncomeForm
from .helpers import *


# load current month tx for selected category
@login_required
def category(request, category):
    cat = Category.objects.get(category=category)
    tx = Expense.objects.filter(user=request.user).filter(date__year=request.session['selected_date'].year).filter(date__month=request.session['selected_date'].month).filter(category=cat)
    context = {'transaction_list': tx}
    return render(request, 'record/tx_list.html', context=context)


@login_required
@permission_required('record.delete_expense', login_url='record:transactions')
def delete(request, tx_id=None):
    # if no tx_id, tx_id does not exist or user mismatch then do not process request
    try:
        if tx_id == None or request.user != Expense.objects.get(pk=tx_id).user:
            return HttpResponseRedirect(reverse('record:index'))
    except:
            return HttpResponseRedirect(reverse('record:index'))

    if request.method == 'POST':
        if request.user == Expense.objects.get(pk=tx_id).user:
            Expense.objects.get(pk=tx_id).delete()
            return HttpResponseRedirect(reverse('record:index'))

        context = {'form': form, 'tx_id': tx_id, 'message': 'Error, user id mismatch.', 'message_type': 'danger'}
        return render(request, 'record/edit.html', context=context)

    return HttpResponseRedirect(reverse('record:index'))


@login_required
@permission_required('record.edit_expense', login_url='record:transactions')
def edit(request, tx_id=None):
    # if no tx_id, tx_id does not exist or user mismatch then do not process request
    try:
        if tx_id == None or request.user != Expense.objects.get(pk=tx_id).user:
            return HttpResponseRedirect(reverse('record:index'))
    except:
            return HttpResponseRedirect(reverse('record:index'))

    e = Expense.objects.get(pk=tx_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=e)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('record:transactions'))
        context = {'form': form, 'tx_id': tx_id, 'message': 'Error, invalid input.', 'message_type': 'danger'}
        return render(request, 'record/edit.html', context=context)

    form = ExpenseForm(instance=e)
    context = {'form': form, 'form_type': 'edit', 'tx_id': tx_id}
    return render(request, 'record/record.html', context=context)


@login_required
@permission_required('record.add_expense', login_url='record:transactions')
def expense(request):
    # save new transaction information to database or load expense form
    if request.method == 'POST':
        # expense submission
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # save the input
            amount = form.cleaned_data['amount']
            tx_date = form.cleaned_data['date']
            category = form.cleaned_data['category']
            method = form.cleaned_data['method']
            comment = form.cleaned_data['comment']
            tag = form.cleaned_data['tag']
            user = request.user

            # only save as USD, but note what the original amount was
            # also store original amount and flip converted to true
            if amount.currency != Currency('USD'):
                fxamount = amount
                converted = True
                comment = comment + ' *ORIGINAL [' + str(amount) + ']*'
                amount = convert_money(amount, 'USD')
                e = Expense.objects.create(amount=amount, date=tx_date, category=category, method=method, comment=comment, tag=tag, user=user, fxamount=fxamount, converted=converted)
            else:
                # otherwise store as submitted
                e = Expense.objects.create(amount=amount, date=tx_date, category=category, method=method, comment=comment, tag=tag, user=user)

            # change to new month, if different from current. also adds new month to navbar
            set_month(request, tx_date.year, tx_date.month)

            # load the index page
            return HttpResponseRedirect(reverse('record:index'))

        context = {'message': f'Error. Form did not properly validate. Errors: {form.errors}', 'message_type': 'danger'}
        return render(request, 'record/index.html', context=context)

    # if not POST, load form
    context = {'form': ExpenseForm(), 'form_type': 'expense'}
    return render(request, 'record/record.html', context=context)


@login_required
@permission_required('record.add_income', login_url='record:index')
def income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            tx_date = form.cleaned_data['date']
            source = form.cleaned_data['source']
            user = request.user

            # only save as USD, but note what the original amount was
            # also store original amount and flip converted to true
            if amount.currency != Currency('USD'):
                fxamount = amount
                converted = True
                amount = convert_money(amount, 'USD')
                i = Income.objects.create(amount=amount, date=tx_date, source=source, user=user, fxamount=fxamount, converted=converted)
            else:
                i = Income.objects.create(amount=amount, date=tx_date, source=source, user=user)

            return HttpResponseRedirect(reverse('record:index'))

    context = {'form': IncomeForm(), 'form_type': 'income'}
    return render(request, 'record/record.html', context=context)


# load main overview screen. redirect to login if needed. set to current month
@login_required
def index(request):
    if not request.session.get('initialize', False):
        request.session['initialize'] = True
        set_month(request, date.today().year, date.today().month)

    transactions = fetch_transactions(request, request.session['selected_date'].year, request.session['selected_date'].month)
    category2D = category_barchart(request)

    context = {'chart': category2D.render(), 'total_month': transactions['total'], 'total_categories': transactions['total_categories'], 'total_year': transactions['total_year']}
    return render(request, 'record/index.html', context=context)


# change selected_date
@login_required
def set_month(request, year, month):
    # set month
    request.session['selected_date'] = date(year, month, 1)

    # add month to navbar if new
    if month not in request.session.get('months', []):
        request.session['months'] = Expense.objects.filter(user=request.user).dates('date', 'month').order_by('-datefield')

    return HttpResponseRedirect(reverse('record:index'))


# load list of transactions
@login_required
def transactions(request):
    tx = Expense.objects.filter(user=request.user).filter(date__year=request.session['selected_date'].year).filter(date__month=request.session['selected_date'].month)
    context = {'transaction_list': tx}
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


@login_required
def ulogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('record:login'))
