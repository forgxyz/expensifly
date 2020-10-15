from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from djmoney.models.fields import CurrencyField, MoneyField
from djmoney.models.validators import BaseMoneyValidator

class Category(models.Model):
    # this won't change or have user input... different type?
    category = models.CharField(max_length=50)

    class Meta:
        # order categories alphabetically
        ordering = ['category']

    def __str__(self):
        return self.category


class Method(models.Model):
    # categorical type?
    method = models.CharField(max_length=50)

    def __str__(self):
        return self.method


class Expense(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    method = models.ForeignKey(Method, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=250, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.category} for {self.amount} on {self.date}"


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['method'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})
        self.fields['tag'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Expense
        fields = ('amount', 'date', 'category', 'method', 'comment', 'tag')
        help_texts = {
            'amount': 'amount will be saved as USD. if converted, original currency and amount will be appended to comment. exchange rates update weekly courtesy of fixer.io',
            'comment': '225 char max.',
            'tag': 'add #tags. 150 char max.'
        }
