from django.db import models
from django.forms import ModelForm
from django.utils import timezone

# Create your models here.

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
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    method = models.ForeignKey(Method, on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=100, blank=True)
    tag = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.comment} for ${self.amount} on {self.date}"


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'method', 'comment', 'tag']
