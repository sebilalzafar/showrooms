from django.shortcuts import render,redirect,get_object_or_404
from core.models import * 
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib import messages
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth.decorators import *
from django.views.decorators.cache import cache_control
from core.forms import ProductForm , SettingsForm
from django.core.mail import send_mail as mail
from django.conf import settings as conf_settings

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def all_orders(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        products = Product.objects.filter(showroom = showroom)
        filter_status = request.GET.get('status', 'all')
        if filter_status == 'all':
            orders = Order.objects.filter(showroom=showroom , ordered = True).order_by('-created_at')
        elif filter_status == 'accepted':
            orders = Order.objects.filter(showroom=showroom,accepted=True , delivered=False).order_by('-created_at')
        elif filter_status == 'rejected':
            orders = Order.objects.filter(showroom=showroom,rejected=True).order_by('-created_at')
        elif filter_status == 'delivered':
            orders = Order.objects.filter(showroom=showroom,delivered=True , accepted = True).order_by('-created_at')
        else:
            orders = Order.objects.none()
        order_data = []
        for order in orders:
            try:
                transaction = Transaction.objects.get(order=order)
                order_data.append({
                    'transaction_id': transaction  # Adjust the field name as needed
                })
            except Transaction.DoesNotExist:
                # Handle the case where no transaction is found
                pass
        context = {
            "showroom": showroom,
            "products": products,
            "orders": orders,
            "order_data": order_data,
            'filter_status': filter_status,
        }
        return render(request , "shop/dashboard/all_orders.html" , context)
    else:
        return redirect("shop_dashboard_signin")
    


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def invoice_order(request,order_id):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        try:
            settings = showroom_settings.objects.get(showroom=showroom)
        except:
            settings=None
        products = Product.objects.filter(showroom = showroom)
        order_detail = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order_detail)
        transaction = Transaction.objects.get(order=order_detail)
        total = sum(item.product.new_price * item.quantity for item in order_items)
        context = {
            "showroom": showroom,
            "products": products,
            "order_detail": order_detail,
            "order_items": order_items,
            "total": total,
            "settings": settings,
            "transaction": transaction,
        }
        return render(request , "shop/dashboard/invoice.html" , context)
    else:
        return redirect("shop_dashboard_signin")

    



@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def reject_order(request, order_id):
    a= request.GET.get('next','')
    order_detail = Order.objects.get(id=order_id)
    order_detail.rejected = True
    order_detail.save()
    
    #message = 'Your order has been submitted to , We will Contact in 24 hours .',
    subject = 'Your order rejection.'
    from_email = conf_settings.EMAIL_HOST_USER
    message = "Your Order has been cancelled due to some reason."
    recipient_list = [order_detail.email]
        
    mail(subject, message, from_email, recipient_list , fail_silently=True)
    messages.success(request,"Order has been rejected and mail has been sent to customer.")
    
    return HttpResponseRedirect(a)


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def accept_order(request, order_id):
    a= request.GET.get('next','')
    order_detail = Order.objects.get(id=order_id)
    order_detail.accepted = True
    order_detail.save()
    
    ##message = 'Your order has been submitted to , We will Contact in 24 hours .',
    #subject = 'Your order confirmation'
    #from_email = conf_settings.EMAIL_HOST_USER
    #message = "Your Order has been accepted .We will contact you soon."
    #recipient_list = [order_detail.email]
        
    #mail(subject, message, from_email, recipient_list , fail_silently=True)
    messages.success(request,"Order has been accepted.")
    
    return HttpResponseRedirect(a)


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def deliver_order(request, order_id):
    a= request.GET.get('next','')
    order_detail = Order.objects.get(id=order_id)
    transaction = Transaction.objects.get(order=order_detail)
    if request.method == "POST":
        email_message = request.POST.get("email_message") 
        total_payable = request.POST.get("total_payable") 
        shipping_amount = request.POST.get("shipping_amount") 
        transaction.amount = total_payable
        transaction.shipping_amount = shipping_amount
        transaction.save()
        
  
        order_detail.delivered = True
        order_detail.save()
    
        ##message = 'Your order has been submitted to , We will Contact in 24 hours .',
        #subject = 'Your order confirmation'
        #from_email = conf_settings.EMAIL_HOST_USER
        #message = "Your Order has been accepted .We will contact you soon."
        #recipient_list = [order_detail.email]
            
        #mail(subject, message, from_email, recipient_list , fail_silently=True)
        messages.success(request,"Order has been delivered.")
    
        return HttpResponseRedirect(a)



    
@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def transaction_details(request):
    showroom = Showrooms.objects.get(id=request.user.id)
    if request.user.showroom_owner == True:
        try:
            settings = showroom_settings.objects.get(showroom=showroom)
        except:
            settings=None
        filter_status = request.GET.get('status', 'all')
        if filter_status == 'all':
            transaction = Transaction.objects.filter(order__showroom=showroom, order__delivered=True).order_by('-order__created_at')
        elif filter_status == 'received':
            transaction = Transaction.objects.filter(order__showroom=showroom, status="RECEIVED", order__delivered=True).order_by('-order__created_at')
        elif filter_status == 'pending':
            transaction = Transaction.objects.filter(order__showroom=showroom, status="PENDING", order__delivered=True).order_by('-order__created_at')
        else:
            transaction = Transaction.objects.none()
        
        
        total_transaction_amount = Transaction.objects.filter(order__showroom = showroom , order__delivered =True)
        total_transaction_amount = sum(item.amount for item in total_transaction_amount)
        pending_transaction_amount = Transaction.objects.filter(order__showroom = showroom , status="PENDING",order__delivered =True)
        pending_transaction_amount = sum(item.amount for item in pending_transaction_amount)
        recieved_transaction_amount = Transaction.objects.filter(order__showroom = showroom , status="RECIEVED",order__delivered =True)
        recieved_transaction_amount = sum(item.amount for item in recieved_transaction_amount)

        context = {
            "showroom": showroom,
            "settings": settings,
            "transaction": transaction,
            "filter_status": filter_status,
            "pending_transaction_amount": pending_transaction_amount,
            "recieved_transaction_amount": recieved_transaction_amount,
            "total_transaction_amount": total_transaction_amount,
            
        }
        return render(request , "shop/dashboard/transactions_reports.html" , context)
    else:
        return redirect("shop_dashboard_signin")
    

def make_paid(request,transaction_id):
    a= request.GET.get('next','')
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    transaction.status = "RECIEVED"
    transaction.save()
    messages.success(request,"Transaction updated successfully")
    return HttpResponseRedirect(a)
    