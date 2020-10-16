# Generated by Django 3.1.1 on 2020-10-16 00:11

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0011_income_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='converted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='fxamount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='expense',
            name='fxamount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('GBP', 'Pound Sterling'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='income',
            name='converted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='income',
            name='fxamount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='income',
            name='fxamount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('GBP', 'Pound Sterling'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
    ]
