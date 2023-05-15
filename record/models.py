from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from djmoney.models.fields import MoneyField


class Category(models.Model):
    category = models.CharField(max_length=50)

    class Meta:
        # order categories alphabetically
        ordering = ['category']

    def __str__(self):
        return self.category


class Method(models.Model):
    method = models.CharField(max_length=50)

    def __str__(self):
        return self.method


class Source(models.Model):
    source = models.CharField(max_length=50)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['source']


class Expense(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    method = models.ForeignKey(Method, on_delete=models.PROTECT)
    comment = models.CharField(max_length=250, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fxamount = MoneyField(max_digits=19, decimal_places=2, null=True, default=None)
    converted = models.BooleanField(default=False)
    budgeted = models.BooleanField(default=False)
    reimbursable = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.category} for {self.amount} on {self.date}"


class Income(models.Model):
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    date = models.DateField(default=timezone.now)
    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fxamount = MoneyField(max_digits=19, decimal_places=2, null=True, default=None)
    converted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} on {self.date}"
