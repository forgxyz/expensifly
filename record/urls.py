from django.urls import path

from . import views

# application namespace
app_name = 'record'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>', views.set_month, name='change_month'),
    path('record', views.record, name='record'),
    path('save', views.save, name='save'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/edit', views.transactions, name='edit_no'),
    path('transactions/delete', views.transactions, name='delete_no'),
    path('transactions/edit/<int:tx_id>', views.edit, name='edit'),
    path('transactions/delete/<int:tx_id>', views.delete, name='delete'),
    path('transactions/<str:category>', views.category, name='category'),    
    path('login/', views.ulogin, name='login'),
    path('logout', views.ulogout, name='logout'),
]
# in template: {% url 'record:index' %}
