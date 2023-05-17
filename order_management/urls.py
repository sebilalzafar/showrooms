from django.urls import path,include
from django.contrib import admin
from order_management import views
urlpatterns = [
    
path('shop-dashboard/all-orders', views.all_orders, name="all_orders"),
path('shop-dashboard/invoice/<str:order_id>', views.invoice_order, name="invoice_order"),
    
    
]