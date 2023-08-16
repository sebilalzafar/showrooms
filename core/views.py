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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers




def home(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password,)
        if user is not None:
            auth_login(request,user)
            messages.success(request,'You are authenticated.')
            return redirect(request.path)
            
        else:
            messages.error(request,'Invalid Credentials.')
            return redirect(request.path)


    l = Showrooms.objects.filter(showroom_type = "Lights").count()
    t = Showrooms.objects.filter(showroom_type = "Tiles").count()
    ac = Showrooms.objects.filter(showroom_type = "Art and Culture").count()
    c = Showrooms.objects.filter(showroom_type = "Cars").count()
    s = Showrooms.objects.filter(showroom_type = "Sanitary").count()
    sw = Showrooms.objects.filter(showroom_type = "Sanitary Ware").count()
    cb = Showrooms.objects.filter(showroom_type = "Chip Board").count()
    pp = Showrooms.objects.filter(showroom_type = "PVC Piping").count()
    ms = Showrooms.objects.filter(showroom_type = "Marble Stone").count()
    context = {
        'l':l,
        't':t,
        'ac':ac,
        'c':c,
        's':s,
        'sw':sw,
        'cb':cb,
        'pp':pp,
        'ms':ms,
    }         
    return render(request, 'index.html',context)

def signup(request):
    if request.method == 'POST':
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exist.Sorry for inconvenience")
            return redirect(request.path)

        else:
            user = User.objects.create_user(first_name=f_name,last_name=l_name,email=email,password=password)
            user.save()
            auth_login(request,user)
            messages.success(request,'You are authenticated.')
            return redirect(request.path)

            
          
    return redirect(request.path)


def check_email(request):
    email = request.POST.get('email')

    if User.objects.filter(email=email).exists():
        return HttpResponse('<div style="color: red"> This email already exists </div>')
    else:
        return HttpResponse('<div style="color: green"> Available</div>')






def showrooms(request):
    title = request.POST.get('title')
    a = Showrooms.objects.filter(showroom_type=title)
    context={
        'a':a,
        'title':title,
    }
    return render(request,"partials/showroom_card.html",context)


def link_360_and_shop(request , pk):
    showroom_data = Showrooms.objects.get(id=pk)
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password,)
        if user is not None:
            auth_login(request,user)
            messages.success(request,'You are authenticated.')
            return redirect(request.path)
            
        else:
            messages.error(request,'Invalid Credentials.')
            return redirect(request.path)
    context={
        'showroom_data':showroom_data,
    }
    return render(request,"360.html",context)



#==================================Shop User===================================
@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def shop(request,pk,id):
        showroom = Showrooms.objects.get(id=id)
        try:
            settings = showroom_settings.objects.get(showroom=showroom)
        except:
            settings=None
        categories = Categories.objects.filter(showroom_type = showroom.showroom_type)
        product = Product.objects.filter(showroom=showroom)
        context = {
            
            'categories':categories,
            'product':product,
            'showroom':showroom,
            'settings':settings,
        }
        return render(request,"shop/products.html",context)


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def shop_cart(request,showroom_id):
    showroom = Showrooms.objects.get(id=showroom_id)
    try:
        settings = showroom_settings.objects.get(showroom=showroom)
    except:
        settings=None
    if Order.objects.filter(user=request.user , showroom = showroom , ordered=False).exists():
        order = Order.objects.get(user=request.user , showroom = showroom , ordered=False)
        order_items = OrderItem.objects.filter(order=order )
        subtotal = sum(item.product.new_price * item.quantity for item in order_items)
        context = {
            'order_items':order_items,
            'showroom':showroom,
            'subtotal':subtotal,
            'settings':settings,
        }
        return render(request,"shop/cart.html",context)
    else:
        context = {
            'showroom':showroom,
            'empty':"Empty Cart",
            'settings':settings,
            
        }
        messages.error(request,"You have an Empty Cart")
        return render(request,"shop/cart.html",context)
    

@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def checkout(request,showroom_id):    
    try:
        showroom = Showrooms.objects.get(id=showroom_id)
        try:
            settings = showroom_settings.objects.get(showroom=showroom)
        except:
            settings=None
        if Order.objects.filter(user=request.user , showroom = showroom , ordered=False).exists():
            order = Order.objects.get(user=request.user , showroom = showroom , ordered=False)
            order_items = OrderItem.objects.filter(order=order )
           
            
            subtotal = sum(item.product.new_price * item.quantity for item in order_items)
            context = {
                'order_items':order_items,
                'showroom':showroom,
                'subtotal':subtotal,
                'order':order,
                'settings':settings,
            }
            return render(request,"shop/checkout.html",context)
        else:
            return redirect("shop_cart")
    except:
        return redirect("home")


        
        
#====================CART and order item fuctionality functionaity=================================




@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def add_to_cart(request, product_id , showroom_id):
    showroom = Showrooms.objects.get(id=showroom_id)
    product = get_object_or_404(Product, pk=product_id)
    order, created = Order.objects.get_or_create(user=request.user,showroom = showroom, ordered=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()
        #messages.success(request, f"{product.title} quantity updated in cart.")
        return HttpResponse("Updated")
        
    else:
        #messages.success(request, f"{product.title} added to cart.")
        return HttpResponse("Added")


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def add_to_cart_in_cart(request, product_id ):
    a= request.GET.get('next','')
    product = get_object_or_404(Product, pk=product_id)
    order_item, created = OrderItem.objects.get_or_create(order__user=request.user.id, product=product , order__ordered = False)
    if not created:
        order_item.quantity += 1
        order_item.save()
        #messages.success(request, f"{product.title} quantity updated in cart.")
        return HttpResponseRedirect(a)

        
    else:
        #messages.success(request, f"{product.title} added to cart.")
        return HttpResponseRedirect(a)



@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def remove_from_cart(request, product_id):
    a= request.GET.get('next','')
    product = get_object_or_404(Product, pk=product_id)
    order_item = OrderItem.objects.filter(order__user=request.user.id, product=product).first()
    if order_item:
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
            #messages.success(request, f"{product.title} quantity updated in cart.")
        else:
            order_item.delete()
            #messages.info(request, f"{product.title} removed from cart.")
    return HttpResponseRedirect(a)


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def delete_from_cart(request, product_id):
    a = request.GET.get('next','')
    product = get_object_or_404(Product, pk=product_id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    order_item = OrderItem.objects.filter(order = order.pk, product=product.id)
    if order_item:
            order_item.delete()
            messages.info(request, f"{product.title} removed from cart.")
    return HttpResponseRedirect(a)




@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='home')
def complete_order(request, order_id):          
        
    if request.method == "POST":
        a = Order.objects.get(pk=order_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        street_address = request.POST.get("street_address")
        city = request.POST.get("city")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        order_description = request.POST.get("order_description")
        total_amount = request.POST.get("total_amount")
        a.first_name = first_name
        a.last_name = last_name
        a.street_address = street_address
        a.city = city
        a.phone = phone
        a.email = email
        a.order_description = order_description
        a.ordered = True
        # Create a list of product names
        product_names = []
        order_products = OrderItem.objects.filter(order=a)
        for order_product in order_products:
            product_names.append(f'{order_product.product.title} * {order_product.quantity}')
        # Update the Order's products field with the list of product names
        a.products_list = ', '.join(product_names)
        a.total_amount = total_amount
        a.save()
        
        
        subject = 'Your order confirmation'
        #message = 'Your order has been submitted to , We will Contact in 24 hours .',
        from_email = conf_settings.EMAIL_HOST_USER
        recipient_list = [a.email]
        
        #mail(subject, str(message), from_email, recipient_list , fail_silently=False)
        
        # Render the email template with dynamic content
        html_content = render_to_string('email_template.html', {
            'recipient_name': first_name,
            'products_list': a.products_list,
            'office_phone_number': a.showroom.office_phone_number,
        })
        # Create the email message with HTML content
        email = EmailMultiAlternatives(subject, body=html_content, from_email=from_email, to=recipient_list , )
        email.attach_alternative(html_content, "text/html")
        # Send the email
        sent = email.send(fail_silently = False)
        if sent == 1:
            print("Email sent successfully.")
        else:
            print("Failed to send email.")
        
        return render(request,"shop/order_confirmation.html")
    else:
        return redirect("home")
    

        
        
#=============================================admin shop and dashboard

def shop_dashboard_signin(request):
     if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password,)
        if user is not None:
            auth_login(request,user)
            if request.user.showroom_owner == True:
                messages.success(request,'You are authenticated as showroom owner.')
                return redirect("shop_dashboard")
            else:
                 messages.error(request,'Invalid credentials for showroom owner.')
                
        else:
            messages.error(request,'Invalid Credentials.')
     
     return render(request , "shop/dashboard/dashboard_signin.html")




@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def shop_dashboard(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        #Total products filters
        total_products = Product.objects.filter(showroom = showroom).count()
        monthly_products = Product.objects.filter(showroom = showroom ,created_at__month=current_month).count()
        yearly_products = Product.objects.filter(showroom = showroom , created_at__year=current_year).count()
        
        #Total orders Filters
        total_orders = Order.objects.filter(showroom=showroom).count()
        monthly_orders = Order.objects.filter(showroom = showroom ,created_at__month=current_month).count()
        pending_orders = Order.objects.filter(showroom = showroom , accepted =True, delivered = False).count()
        
        context = {
            "showroom": showroom,
            "total_products": total_products,
            "monthly_products": monthly_products,
            "yearly_products": yearly_products,
            
            "total_orders": total_orders,
            "monthly_orders": monthly_orders,
            "pending_orders": pending_orders,
        }
        return render(request , "shop/dashboard/dashboard.html" ,context)
    else:
        return redirect("shop_dashboard_signin")



@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def node_info(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        
        context = {
            "showroom": showroom,
  
        }
        return render(request , "shop/dashboard/node_info.html" ,context)
    else:
        return redirect("shop_dashboard_signin")
    
    
def node_info_update(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        all_nodes = Node_visitors.objects.filter(showroom=showroom)
           # Convert the data to a JSON response
               # Prepare the data as a list of dictionaries
        data = [
            {
                'user': f"{node.user.first_name} {node.user.last_name}" ,
                'node': node.node,
                'link': f"{showroom.link_360}?node={node.node}"

            }
            for node in all_nodes
        ]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)
        
    



def node_visitor(request):
    if request.method == "POST":
        node_id  = request.POST.get("currentNodeID")
        user_id  = request.POST.get("userID")
        showroom_id  = request.POST.get("showroomID")
        node ,created= Node_visitors.objects.get_or_create(showroom=Showrooms.objects.get(id=showroom_id), user=User.objects.get(id=user_id) )
        node.node = node_id
        node.save()
        
        node_info_update(request)
        return HttpResponse(status=204)  # 204 No Content

        
    



@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def google_analytics(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        context = {
            "showroom": showroom,
        }
        return render(request , "shop/dashboard/ga.html" ,context)
    else:
        return redirect("shop_dashboard_signin")


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def all_companies(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        all_companies = Company_name.objects.filter(showroom_type = showroom.showroom_type)
        if request.method == "POST":
            showroom_type = request.POST.get('showroom_type')
            company_name = request.POST.get('company_name')
            
            if Company_name.objects.filter(name__iexact=company_name).exists():
                messages.error(request,"Company name already exists.")
                return redirect(request.path)
                
            else:
                Company_name.objects.create(showroom_type = showroom_type, name = company_name)
                messages.success(request,"Company name added.")
                return redirect(request.path)
                
        context = {
            "showroom": showroom,
            "all_companies": all_companies,

        }
        return render(request , "shop/dashboard/companies.html" ,context)
    else:
        return redirect("shop_dashboard_signin")



def check_company(request):
    company_name = request.POST.get('company_name').lower()

    if Company_name.objects.filter(name__iexact=company_name).exists():
        return HttpResponse('<div style="color: red"> This company name already exists. </div>')
    else:
        return HttpResponse('<div style="color: green"> You can add this now.</div>')





@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def all_categories(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        all_categories = Categories.objects.filter(showroom_type = showroom.showroom_type)
        if request.method == "POST":
            showroom_type = request.POST.get('showroom_type')
            category_name = request.POST.get('category_name')
            
            if Categories.objects.filter(name__iexact=category_name).exists():
                messages.error(request,"Category already exists.")
                return redirect(request.path)
                
            else:
                Categories.objects.create(showroom_type = showroom_type, name = category_name)
                messages.success(request,"Category added.")
                return redirect(request.path)
                
        context = {
            "showroom": showroom,
            "all_categories": all_categories,

        }
        return render(request , "shop/dashboard/categories.html" ,context)
    else:
        return redirect("shop_dashboard_signin")



def check_category(request):
    category_name = request.POST.get('category_name').lower()

    if Categories.objects.filter(name__iexact=category_name).exists():
        return HttpResponse('<div style="color: red"> This category already exists. </div>')
    else:
        return HttpResponse('<div style="color: green"> You can add this category.</div>')





@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def all_products(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        products = Product.objects.filter(showroom = showroom)
        context = {
            "showroom": showroom,
            "products": products,
        }
        return render(request , "shop/dashboard/product_list.html" ,context)
    else:
        return redirect("shop_dashboard_signin")
        
        
@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')        
def add_product(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
      
        if request.method == 'POST':
            form = ProductForm( request.user,request.POST, request.FILES )
            if form.is_valid():
                fm = form.save(commit = False)
                fm.showroom = showroom
                fm.save()
                messages.success(request,"Product Added Succesfully.")
                return redirect('all_products')
        else:
            form = ProductForm(request.user)
            context = {
            "showroom": showroom,
            'form': form
                                }
            return render(request, 'shop/dashboard/add_product.html', context)
    else:
        return redirect("shop_dashboard_signin")




@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def update_product(request , id):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        product = Product.objects.get(id=id)

        if request.method == 'POST':
            form = ProductForm( request.user,request.POST, request.FILES , instance=product)
            if form.is_valid():
                fm = form.save(commit = False)
                fm.showroom = showroom
                fm.save()
                messages.success(request,"Product Updated Succesfully.")
                return redirect('all_products')
        else:
            form = ProductForm( request.user,instance=product)
            context = {
            "showroom": showroom,
            'form': form
                                }
            return render(request, 'shop/dashboard/update_product.html', context)
    else:
        return redirect("shop_dashboard_signin")


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def delete_product(request , id):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        product = get_object_or_404(Product, pk=id)
        if request.method == 'POST':
            product.delete()
            messages.success(request,"Product deleted Succesfully.")
            
            return redirect("all_products")

   
        context = {
        "showroom": showroom,
        "product": product,
                            }
        return render(request, 'shop/dashboard/delete_product.html', context)
    else:
        return redirect("shop_dashboard_signin")


@cache_control(no_cache=True, must_revalidate=True , no_store=True)
@login_required(login_url='shop_dashboard_signin')
def settings(request):
    if request.user.showroom_owner == True:
        showroom = Showrooms.objects.get(id=request.user.id)
        
        if showroom_settings.objects.filter(showroom=showroom).exists():
            instance = showroom_settings.objects.get(showroom=showroom)
        else :
            instance = None
        if request.method == 'POST':
            form = SettingsForm( request.POST, request.FILES,  instance=instance )
            if form.is_valid():
                fm = form.save(commit = False)
                fm.showroom = showroom
                fm.save()
                messages.success(request,"Configration Updated")
        else:
            form = SettingsForm(instance=instance)
        context = {
        "showroom": showroom,
        'form': form,
        'instance': instance,
        }
        return render(request, 'shop/dashboard/settings.html', context)
    else:
        return redirect("shop_dashboard_signin")



def dashboard_logout(request):
    django_logout(request)
    messages.error(request,"Logged Out.")
    return redirect('shop_dashboard_signin')




#             end admin shop and dashboard


def callback(request):
    if request.method == 'POST':
        showroom = request.POST.get("showroom")
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("number")
        reason = request.POST.get("reason")
        time = request.POST.get("time")
        a = Callback.objects.create(showroom=Showrooms.objects.get(id=showroom) , person_name=name, 
                                    email=email, phone=phone, reason=reason, time=time)
        a.save()
        return HttpResponse('<h4>Your request has been submitted.We will contact you soon.</h4>')


#@cache_control(no_cache=True, must_revalidate=True , no_store=True)
#@login_required(login_url='home')





def logout(request):
    django_logout(request)
    messages.error(request,"Logged Out.")
    return redirect('home')







    


        

        








            
            


