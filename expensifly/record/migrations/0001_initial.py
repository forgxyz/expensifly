# Generated by Django 3.0.3 on 2020-07-30 15:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='record.Category')),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='record.Method')),
            ],
        ),
    ]
