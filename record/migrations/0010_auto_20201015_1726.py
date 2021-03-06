# Generated by Django 3.1.1 on 2020-10-15 21:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0009_auto_20201015_1533'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='record.category'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='comment',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='expense',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='record.method'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='tag',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('GBP', 'Pound Sterling'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, max_digits=19)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='record.source')),
            ],
        ),
    ]
