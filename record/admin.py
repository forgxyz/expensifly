from django.contrib import admin
from .models import Method, Category, Expense

# Register your models here.
admin.site.register(Method)
admin.site.register(Category)
admin.site.register(Expense)
