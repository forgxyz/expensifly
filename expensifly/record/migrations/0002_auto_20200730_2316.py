# Generated by Django 3.0.3 on 2020-07-31 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='comment',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='expense',
            name='tag',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
