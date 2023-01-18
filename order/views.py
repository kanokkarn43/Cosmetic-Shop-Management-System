from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse

from django.forms.models import model_to_dict

from django.db import connection

from order.models import * 
import json

# Create Order views
def index(request):
    data = {}
    return render(request, 'order/order.html', data)

def AllOrder(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * '
                    ' FROM all_order '
                    ' ORDER By order_id')                    
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name

    return render(request, 'order/all_order.html', data_report)

class OrderList(View):
    def get(self, request):
        all_orders = list(Order.objects.all().values())
        data = dict()
        data['all_orders'] = all_orders
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response 

class OrderDetail(View):
    def get(self, request, pk):
        all_order = get_object_or_404(Order, pk=pk)
        data = dict()
        data['all_orders'] = model_to_dict(all_order) 
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response   


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result             
      