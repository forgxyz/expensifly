from django.contrib import admin
from .models import Method, Category, Expense, Source, Income

# Register your models here.
admin.site.register(Method)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Source)
admin.site.register(Income)
