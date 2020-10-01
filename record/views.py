from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from datetime import date
from django_pandas.io import read_frame

from .models import Category, Expense, ExpenseForm


# load current month tx for selected category
@login_required
def category(request, category):
    cat = Category.objects.get(category=category)
    tx = Expense.objects.filter(date__year=request.session['selected_date'].year).filter(date__month=request.session['selected_date'].month).filter(category=cat)
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
            set_month(request, request.session['selected_date'].year, request.session['selected_date'].month)
            return HttpResponseRedirect(reverse('record:transactions'))

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
            set_month(request, form.cleaned_data['date'].year, form.cleaned_data['date'].month)
            return HttpResponseRedirect(reverse('record:transactions'))
        context = {'form': form, 'tx_id': tx_id, 'message': 'Error, invalid input.', 'message_type': 'danger'}
        return render(request, 'record/edit.html', context=context)

    form = ExpenseForm(instance=e)
    context = {'form': form, 'tx_id': tx_id}
    return render(request, 'record/edit.html', context=context)


# load main overview screen. redirect to login if needed. set to current month
@login_required
def index(request):
    if not request.session.get('initialize', False):
        request.session['initialize'] = True
        set_month(request, date.today().year, date.today().month)
    return render(request, 'record/index.html')


# load Expense ModelForm
@login_required
def record(request):
    context = {'form': ExpenseForm()}
    return render(request, 'record/record.html', context=context)


# handle Expense ModelForm submission
@login_required
@permission_required('record.add_expense', login_url='record:transactions')
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

            e = Expense.objects.create(amount=amount, date=sel_date, category=category, method=method, comment=comment, tag=tag, user=request.user)

            # change to new month, if different from current. also adds new month to navbar
            set_month(request, sel_date.year, sel_date.month)
        return HttpResponseRedirect(reverse('record:index'))

    # if not POST, redirect to form load
    return HttpResponseRedirect(reverse('record:record'))

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.


# change selected_date
@login_required
def set_month(request, year, month):
    # set month
    request.session['selected_date'] = date(year, month, 1)

    # load tx for this user id
    transactions_month = Expense.objects.filter(user=request.user).filter(date__year=request.session['selected_date'].year).filter(date__month=request.session['selected_date'].month)
    request.session['total_month'] = transactions_month.aggregate(Sum('amount'))['amount__sum']

    request.session['total_year'] = Expense.objects.filter(user=request.user).filter(date__year=request.session['selected_date'].year).aggregate(Sum('amount'))['amount__sum']

    # calc top categories
    tx = read_frame(transactions_month, fieldnames=['category', 'amount'])
    request.session['top_cats'] = tx.groupby('category').sum().sort_values('amount', ascending=False).to_dict()

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
