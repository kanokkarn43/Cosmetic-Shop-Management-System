from decimal import ROUND_DOWN
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection
from datetime import date

#from report.models import *
from salereport.models import * 
import json

# Create your views here.
def index(request):
    return render(request, 'salereport/salereport.html')

def TotalSalesReport(request):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        " FROM all_order "
                        "ORDER BY order_id")               
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    with connection.cursor() as cursor1:
        cursor1.execute('SELECT SUM(amount) as "Sales Total" '
                        ' FROM all_order '
                        )               
                            
        row1 = dictfetchall(cursor1)
        column_name1 = [col[0] for col in cursor1.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name
    data_report['data1'] = row1
    data_report['column_name1'] = column_name1

    return render(request, 'salereport/total_sale_report.html', data_report)

def DailySalesReport(request):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        "FROM all_order "
                        "WHERE order_date = CURRENT_DATE " 
                        )               
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    with connection.cursor() as cursor2:
        cursor2.execute('SELECT SUM(amount) as "Sales Total" '
                        ' FROM all_order '
                        ' WHERE order_date = CURRENT_DATE' )               
                            
        row2 = dictfetchall(cursor2)
        column_name2 = [col[0] for col in cursor2.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name
    data_report['data2'] = row2
    data_report['column_name2'] = column_name2

    return render(request, 'salereport/daily_sale_report.html', data_report)

def ProductSalesReport(request):
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT product_code AS "Product Code" , product_name AS "Product Name", price AS "Unit Price", sold_no AS "Unit Sales" , (price*sold_no) AS "Amount" '
                        'FROM all_product'
                        )               
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]
    
    with connection.cursor() as cursor2:
        cursor2.execute('SELECT SUM(price*sold_no) as "Sales Total" '
                        ' FROM all_product ')               
                            
        row2 = dictfetchall(cursor2)
        column_name2 = [col[0] for col in cursor2.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name
    data_report['data2'] = row2
    data_report['column_name2'] = column_name2

    return render(request, 'salereport/product_sale_report.html', data_report)   


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