# Generated by Django 4.2.1 on 2023-05-15 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0018_rename_discretionary_expense_budgeted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='budgeted',
            field=models.BooleanField(default=False),
        ),
    ]
