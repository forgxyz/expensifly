# Generated by Django 4.2.1 on 2023-05-15 16:35

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0013_auto_20201015_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('ISK', 'Icelandic Króna'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='expense',
            name='fxamount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='fxamount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('ISK', 'Icelandic Króna'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('ISK', 'Icelandic Króna'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='income',
            name='fxamount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='fxamount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('ISK', 'Icelandic Króna'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3, null=True),
        ),
    ]
