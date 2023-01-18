"""lab5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from products import views as products_views
from sale import views as sale_views
from order import views as order_views 
from salereport import views as salereport_views 
from app_users import views as app_users_views 

urlpatterns = [ 
    
    path('admin/', admin.site.urls),
    path('users/', include("app_users.urls")),
    path('', app_users_views.index, name='index'),
    path('app_users', app_users_views.index, name='index'),
    
    # products 
    path('products', products_views.index, name='index'),
    path('products/AllBathAndBody', products_views.AllBathAndBody),
    path('products/AllSkinCare', products_views.AllSkinCare),
    path('products/AllMakeUp', products_views.AllMakeUp),
    path('products/AllFragrances', products_views.AllFragrances),
    path('all_product/list', products_views.AllProductList.as_view(), name='all_product_list'),
    path('all_product/detail/<pk>', products_views.AllProductDetail.as_view(), name='all_productr_detail'),

    # sale 
    path('sale', sale_views.index, name='index'),
    path('all_product/list', sale_views.AllProductList.as_view(), name='all_product_list'),
    path('all_product/detail/<pk>', sale_views.AllProductDetail.as_view(), name='all_productr_detail'),
    path('member/list', sale_views.MemberList.as_view(), name='member_list'),
    path('member/detail/<pk>', sale_views.MemberDetail.as_view(), name='member_detail'),
    path('all_order/list', sale_views.OrderList.as_view(), name='all_order_list'),
    path('all_order/detail/<str:pk>/<str:pk2>', sale_views.OrderDetail.as_view(), name='all_order_detail'),
    path('all_order/create', sale_views.OrderCreate.as_view(), name='all_order_create'),
    path('sale/pdf/<str:pk>', sale_views.OrderPDF.as_view(), name='all_order_pdf'),

    # order 
    path('order', order_views.index, name='index'),
    path('order/AllOrder', order_views.AllOrder),
    path('all_order/list', order_views.OrderList.as_view(), name='all_order_list'),
    path('all_order/detail/<pk>', order_views.OrderDetail.as_view(), name='all_order_detail'),


    # salereport 
    path('salereport', salereport_views.index, name='index'),
    path('salereport/TotalSalesReport', salereport_views.TotalSalesReport),
    path('salereport/DailySalesReport', salereport_views.DailySalesReport),
    path('salereport/ProductSalesReport', salereport_views.ProductSalesReport),
    
    
]

