from django.urls import path,include
from django.contrib import admin
from core import views
urlpatterns = [
    path('', views.home , name='home'),
    path('check_email', views.check_email , name='check_email'),
    path('signup', views.signup , name='signup'),
    path('logout/', views.logout , name='logout'),
    path('showrooms/', views.showrooms , name='showrooms'),
    path('showrooms/360-and-shop/360/<pk>', views.link_360_and_shop , name='360_and_shop'),
    path('callback', views.callback, name="callback"),
    path('showrooms/360-and-shop/shop/<pk>/<id>', views.shop, name="shop"),
    

]
