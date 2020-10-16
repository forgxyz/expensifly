from django import forms

from .models import Expense, Income


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
            'amount': 'amount will be converted to USD',
            'comment': '225 char max.',
            'tag': 'add #tags. 150 char max.'
        }


class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['source'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Income
        fields = ('amount', 'date', 'source')
        help_texts = {
            'amount': 'amount will be converted to USD'
        }
