from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import connection

from sale.models import * 
import json

# Create your views here.
def index(request):
    data = {}
    return render(request, 'sale/sale.html', data) 
 
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

class MemberList(View):
    def get(self, request):
        members = list(Member.objects.all().values())
        data = dict()
        data['members'] = members
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class MemberDetail(View):
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        data = dict()
        data['members'] = model_to_dict(member) 
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response        

class OrderList(View):
    def get(self, request):
        all_orders = list(Order.objects.order_by('order_id').all().values())
        data = dict()
        data['all_orders'] = all_orders
        response = JsonResponse(data)
        
        return response 

class OrderDetail(View):
    def get(self, request, pk, pk2):
        order_id = pk 
        
        all_order = list(Order.objects.select_related("member")
                    .filter(order_id=order_id)
                    .values('order_id', 'order_date', 'contact', 'amount'))
        orderlineitem = list(OrderLineItem.objects.select_related('product_code')
                        .filter(order_id=order_id).order_by('item_no')
                        .values("item_no","order_id","product_code","price","quantity","product_total"))

        data = dict()
        data['all_order'] = all_order[0]
        data['orderlineitem'] = orderlineitem 

        response = JsonResponse(data)
        
        return response   

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = '__all__'        



@method_decorator(csrf_exempt, name='dispatch')
class OrderCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if Order.objects.count() != 0:
            order_id_max = Order.objects.aggregate(Max('order_id'))['order_id__max']
            next_order_id = order_id_max[0:2] + str(int(order_id_max[2:5])+1) 
        else:
            next_order_id = "SL100" 
        request.POST['order_id'] = next_order_id
        request.POST['order_date'] = reFormatDateMMDDYYYY(request.POST['order_date'])
        request.POST['amount'] = reFormatNumber(request.POST['amount'])

        form = OrderForm(request.POST)
        print(request.POST)
        if form.is_valid():
            all_order = form.save()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                product_code = AllProduct.objects.get(pk=lineitem['product_code'])
                OrderLineItem.objects.create(
                    order_id=all_order,
                    item_no=lineitem['item_no'],
                    product_code=product_code,
                    price=reFormatNumber(lineitem['price']),
                    quantity=reFormatNumber(lineitem['quantity']),
                    product_total=reFormatNumber(lineitem['product_total'])
                )

            data['all_order'] = model_to_dict(all_order)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response


@method_decorator(csrf_exempt, name='dispatch')

class OrderPDF(View):
    def get(self, request, pk):
        order_id = pk 

        all_order = list(Order.objects.select_related("member").filter(order_id=order_id)
                    .values('order_id', 'order_date', 'contact', 'amount'))
        orderlineitem = list(OrderLineItem.objects.select_related('product_code')
                        .filter(order_id=order_id).order_by('item_no')
                        .values("item_no","order_id","product_code", "price","quantity","product_total"))
        data = dict()
        data['all_order'] = all_order[0]
        data['orderlineitem'] = orderlineitem
        
        return render(request, 'sale/pdf.html', data)



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")