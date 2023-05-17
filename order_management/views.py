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
            orders = Order.objects.all().order_by('-created_at')
        elif filter_status == 'accepted':
            orders = Order.objects.filter(accepted=True).order_by('-created_at')
        elif filter_status == 'rejected':
            orders = Order.objects.filter(rejected=True).order_by('-created_at')
        elif filter_status == 'delivered':
            orders = Order.objects.filter(delivered=True , accepted = True).order_by('-created_at')
        else:
            orders = Order.objects.none()
        context = {
            "showroom": showroom,
            "products": products,
            "orders": orders,
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
        products = Product.objects.filter(showroom = showroom)
        order_detail = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order_detail)
        total = sum(item.product.new_price * item.quantity for item in order_items)
        context = {
            "showroom": showroom,
            "products": products,
            "order_detail": order_detail,
            "order_items": order_items,
            "total": total,
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
    if request.method == "POST":
        email_message = request.POST.get("email_message",) 
        print(email_message)
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



    
    