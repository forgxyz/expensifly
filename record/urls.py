from django.urls import path

from . import views

# application namespace
app_name = 'record'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>', views.set_month, name='change_month'),
    path('expense', views.expense, name='expense'),
    path('income', views.income, name='income'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/edit', views.transactions, name='edit_no'),
    path('transactions/delete', views.transactions, name='delete_no'),
    path('transactions/edit/<str:tx_type>/<int:tx_id>', views.edit, name='edit'),
    path('transactions/delete/<str:tx_type>/<int:tx_id>', views.delete, name='delete'),
    path('transactions/<str:cat>', views.category, name='category'),
    path('login/', views.ulogin, name='login'),
    path('logout', views.ulogout, name='logout'),
    path('overview', views.overview_portal, name='overview'),
]
# in template: {% url 'record:index' %}
