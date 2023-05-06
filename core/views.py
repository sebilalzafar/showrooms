from django.shortcuts import render,redirect
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
from django.http import Http404

def home(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password,)
        if user is not None:
            auth_login(request,user)
            messages.success(request,'You are authenticated.')
            if request.user.showroom_owner == True:
              return redirect('light_home')
            else:
              return redirect('home')
        else:
            messages.error(request,'Invalid Credentials.')
            HttpResponseRedirect('/')

    l = Showrooms.objects.filter(showroom_type = "lights").count()
    t = Showrooms.objects.filter(showroom_type = "tiles").count()
    ac = Showrooms.objects.filter(showroom_type = "Art and Culture").count()
    c = Showrooms.objects.filter(showroom_type = "Cars").count()
    s = Showrooms.objects.filter(showroom_type = "sanitary").count()
    sw = Showrooms.objects.filter(showroom_type = "sanitary ware").count()
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
        print(f_name,l_name,email,password)
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exist.Sorry for inconvenience")
            return redirect('home')
        else:
            user = User.objects.create_user(first_name=f_name,last_name=l_name,email=email,password=password)
            user.save()
            auth_login(request,user)
            messages.success(request,'You are authenticated.')
            return redirect("home")
            
          
    return redirect("home")


def check_email(request):
    email = request.POST.get('email')

    if User.objects.filter(email=email).exists():
        return HttpResponse('<div style="color: red"> This email already exists </div>')
    else:
        return HttpResponse('<div style="color: green"> Available</div>')



def showrooms(request):
    title = request.POST.get('title')
    print(title)
    a = Showrooms.objects.filter(showroom_type=title)
    context={
        'a':a,
        'title':title,
    }
    return render(request,"partials/showroom_card.html",context)

def link_360_and_shop(request , pk):
    showroom_data = Showrooms.objects.get(id=pk)
    context={
        'showroom_data':showroom_data,
    }
    return render(request,"360.html",context)



#==================================Shop Queries===================================

def shop(request,pk,id):
    try:
        if pk == "Lights":
            categories = Categories.objects.filter(showroom_type = "Lights")
            products = Lights.objects.filter(showroom=id)   
            showroom = Showrooms.objects.get(id=id)
  
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/lights.html",context)
        elif pk == "Tiles":
            categories = Categories.objects.filter(showroom_type = "Tiles")
            products = Tiles.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/tiles.html",context)
        elif pk == "Art and Culture": 
            categories = Categories.objects.filter(showroom_type = "Art and Culture")
            products = Art_And_Culture.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/art_and_culture.html",context)
        
        elif pk == "Cars":
            categories = Categories.objects.filter(showroom_type = "Cars")
            products = Cars.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/cars.html",context)
        elif pk == "Sanitary":
            categories = Categories.objects.filter(showroom_type = "Sanitary")
            products = Sanitary.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/sanitary.html",context)
        elif pk == "Sanitary Ware":
            categories = Categories.objects.filter(showroom_type = "Sanitary Ware")
            products = Sanitary_Ware.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/sanitary_ware.html",context)
        elif pk == "Chip Board":
            categories = Categories.objects.filter(showroom_type = "Chip Board")
            products = Chip_Board.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/chip_board.html",context)
        elif pk == "PVC Piping":
            return render(request,"shop/pvc_piping.html")
        elif pk == "Marble Stone":
            categories = Categories.objects.filter(showroom_type = "Marble Stone")
            products = Marble_Stone.objects.filter(showroom=id)   
            context = {
                'products':products,
                'categories':categories,
            }
            return render(request,"shop/marble_stone.html",context)
    except:
        raise Http404
    else:
      return redirect("home")
        
        



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
#=========================main page with all slips of user


#@cache_control(no_cache=True, must_revalidate=True , no_store=True)
#@login_required(login_url='home')





def logout(request):
    django_logout(request)
    messages.error(request,"Logged Out.")
    return redirect('home')




#====================CART functionaity=================================

def add_to_cart(request,id):
    a= request.GET.get('next','')
    product = Product.objects.get(id = id)
    cart = Cart.objects.filter(user=request.user , product = product.id)
    if cart.exists():
        messages.error(request,"Already exist in cart.")
    else:
        a = Cart.objects.create(user=request.user,product=product)
        a.save()
        print("Product added ")
        
    return HttpResponseRedirect(a)



            
