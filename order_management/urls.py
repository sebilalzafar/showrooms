from django.urls import path,include
from django.contrib import admin
from order_management import views
urlpatterns = [
    
path('shop-dashboard/all-orders', views.all_orders, name="all_orders"),
path('shop-dashboard/invoice/<str:order_id>', views.invoice_order, name="invoice_order"),
path('shop-dashboard/invoice/reject-order/<str:order_id>', views.reject_order, name="reject_order"),
path('shop-dashboard/invoice/accept-order/<str:order_id>', views.accept_order, name="accept_order"),
path('shop-dashboard/invoice/deliver-order/<str:order_id>', views.deliver_order, name="deliver_order"),
path('shop-dashboard/transaction-details', views.transaction_details, name="transaction_details"),
path('shop-dashboard/transaction-details/make-paid/<str:transaction_id>', views.make_paid, name="make_paid"),
    
    
]