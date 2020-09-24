from django.urls import path

from . import views

# application namespace
app_name = 'record'

urlpatterns = [
    path('', views.index, name='index'),
    path('record/', views.record, name='record'),
    path('save', views.save, name='save'),
    path('transactions/', views.transactions, name='transactions'),
    path('overview/<int:year>/<int:month>/', views.change_month, name='change_month'),
]

# in template: {% url 'record:index' %}
