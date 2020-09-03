from django.urls import path

from . import views

# application namespace
app_name = 'view'

urlpatterns = [
    path('<int:year>/<int:month>/', views.index, name='index'),
    path('', views.index, name='index'),
]

# in template: {% url 'viz:index' %}
