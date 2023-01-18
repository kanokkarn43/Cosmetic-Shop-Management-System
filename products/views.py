from decimal import ROUND_DOWN
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse

from django.forms.models import model_to_dict
from django.db import connection

from products.models import * 
import json

# Create products views
def index(request):
    return render(request, 'products/products.html')

def AllBathAndBody(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        " FROM all_product "
                        " WHERE product_code LIKE 'G%' "
                        "ORDER BY product_code")                    
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description] 

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name

    return render(request, 'products/all_bath_and_body.html', data_report)

def AllSkinCare(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        " FROM all_product "
                        " WHERE product_code LIKE 'C%' "
                        "ORDER BY product_code")                    
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name

    return render(request, 'products/all_skincare.html', data_report)

def AllMakeUp(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        " FROM all_product "
                        " WHERE product_code LIKE 'L%' "
                        "ORDER BY product_code")                    
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name

    return render(request, 'products/all_makeup.html', data_report)    

def AllFragrances(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * "
                        " FROM all_product "
                        " WHERE product_code LIKE 'P%' "
                        "ORDER BY product_code")                    
                            
        row = dictfetchall(cursor)
        column_name = [col[0] for col in cursor.description]

    data_report = dict()
    data_report['data'] = row
    data_report['column_name'] = column_name

    return render(request, 'products/all_fragrances.html', data_report)    

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

class AllProductList(View):
    def get(self, request):
        all_products = list(AllProduct.objects.all().values())
        data = dict()
        data['all_products'] = all_products
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response  

class AllProductDetail(View):
    def get(self, request, pk):
        all_product = get_object_or_404(AllProduct, pk=pk)
        data = dict()
        data['all_products'] = model_to_dict(all_product)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response     

    