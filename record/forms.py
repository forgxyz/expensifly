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
        self.fields['budgeted'].widget.attrs.update({'class': 'form-check'})
        self.fields['reimbursable'].widget.attrs.update({'class': 'form-check form-check-inline'})

    class Meta:
        model = Expense
        fields = ('amount', 'date', 'category', 'method', 'comment', 'tag', 'budgeted', 'reimbursable')
        help_texts = {
            'amount': 'amount will be converted to USD',
            'comment': '225 char max.',
            'tag': 'Separate tags by comma. 150 char max.',
            'budgeted': 'Select if the expense was a budgeted purchase, leave unchecked if DISCRETIONARY.'
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
