from django.urls import path

from . import views

# application namespace
app_name = 'record'

urlpatterns = [
    path('', views.index, name='index'),
    path('record/', views.record, name='record'),
    path('save', views.save, name='save'),
    path('view/', views.view_tx, name='view'),
    path('view/<int:year>/<int:month>/', views.view_tx, name='view_tx'),
]

# in template: {% url 'record:index' %}
