from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from datetime import date

from .models import Expense, ExpenseForm
from .helpers import get_spending

# change SELECTED_DATE
def change_month(request, year, month):
    request.session['SELECTED_DATE'] = date(year, month, 1)
    context = get_spending(request.session['SELECTED_DATE'])
    return render(request, 'record/index.html', context=context)

# load main overview screen. if first load, gather months from db and set SELECTED_DATE to current month
def index(request):
    if not request.session.get('initialize', False):
        request.session['initialize'] = True
        request.session['MONTHS'] = Expense.objects.dates('date', 'month').order_by('-datefield')
        request.session['SELECTED_DATE'] = date.today()

    context = get_spending(request.session['SELECTED_DATE'])
    return render(request, 'record/index.html', context=context)


# insight portal
def portal(request):
    context = {}
    return render(request, 'record/portal.html', context=context)


# load Expense ModelForm
def record(request):
    form = ExpenseForm()
    return render(request, 'record/record.html', {'form': form})

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
            if date(sel_date.year, sel_date.month, 1) not in request.session['MONTHS']:
                request.session['MONTHS'] = Expense.objects.dates('date', 'month').order_by('-datefield')

        return HttpResponseRedirect('/')

    # if not POST, load empty form
    else:
        form = ExpenseForm()
    context = {'form': form}
    return render(request, 'record/index.html', context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.

# load list of transactions
def transactions(request):
    context = get_spending(request.session['SELECTED_DATE'])
    return render(request, 'record/tx_list.html', context=context)
