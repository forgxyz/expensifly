from collections import OrderedDict
from django_pandas.io import read_frame

from .models import Expense
from .fusioncharts import *

def category_barchart(request):
    dataSource = {
        "chart": {
            "caption": f"Top Categories For {request.session['selected_date'].year}",
            "theme": "fusion",
        },
        "data": []
    }

    # load data for chart
    transactions = Expense.objects.filter(user=request.user).filter(date__year=request.session['selected_date'].year)

    # calc top categories
    tx = read_frame(transactions, fieldnames=['category', 'amount'])
    top_cats = tx.groupby('category').sum().sort_values('amount', ascending=False).to_dict()

    for cat, amount in top_cats['amount'].items():
        data = {}
        data['label'] = cat
        data['value'] = int(amount)
        dataSource['data'].append(data)

    column2D = FusionCharts("bar2d", "categoryBarChart", "85%", "550", "categoryBarChart-container", "json", dataSource)
    return column2D
