from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from datetime import date

from .models import Expense, ExpenseForm
from .helpers import get_spending

# Create your views here.
def index(request):
    context = get_spending()
    return render(request, 'record/index.html', context=context)


def record(request):
    form = ExpenseForm()
    return render(request, 'record/record.html', {'form': form})


def save(request):
    # save new transaction information to database
    months = Expense.objects.dates('date', 'month')

    if request.method == 'POST':
        # expense submission
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # save the input
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            category = form.cleaned_data['category']
            method = form.cleaned_data['method']
            comment = form.cleaned_data['comment']
            tag = form.cleaned_data['tag']

            e = Expense.objects.create(amount=amount, date=date, category=category, method=method, comment=comment, tag=tag)
            context = {'message': 'Success', 'transaction': e, 'months': months}
        return render(request, 'record/success.html', context)

    else:
        form = ExpenseForm()
    context = {'form': form, 'months': months}
    return render(request, 'record/index.html', context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.


def view_tx(request, year=date.today().year, month=date.today().month):
    context = get_spending()
    return render(request, 'record/tx_list.html', context=context)
