from django.urls import path

from . import views

# application namespace
app_name = 'record'

urlpatterns = [
    path('', views.index, name='index'),
    path('save', views.save, name='save'),
]

# in template: {% url 'record:index' %}
