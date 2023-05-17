from django.urls import path,include
from django.contrib import admin
from core import views
urlpatterns = [
    path('', views.home , name='home'),
    path('check_email', views.check_email , name='check_email'),
    path('signup', views.signup , name='signup'),
    path('logout', views.logout , name='logout'),
    path('showrooms/', views.showrooms , name='showrooms'),
    path('360-and-shop/360/<str:pk>', views.link_360_and_shop , name='360_and_shop'),
    path('callback', views.callback, name="callback"),
    path('360-and-shop/shop/<pk>/<id>', views.shop, name="shop"),
    
    #dashboard
    
    path('shop-dashboard-signin', views.shop_dashboard_signin, name="shop_dashboard_signin"),
    path('dashboard_logout', views.dashboard_logout, name="dashboard_logout"),
    path('shop-dashboard', views.shop_dashboard, name="shop_dashboard"),
    path('settings', views.settings, name="settings"),
    
    
    path('shop-dashboard/add_product', views.add_product, name="add_product"),
    path('shop-dashboard/update_product/<str:id>', views.update_product, name="update_product"),
    path('shop-dashboard/delete_product/<str:id>', views.delete_product, name="delete_product"),
    
    
    
    # cart and order items
    
    path('shop-cart/<str:showroom_id>', views.shop_cart, name='shop_cart'),
    path('add-to-cart/<str:product_id>/<str:showroom_id>', views.add_to_cart, name='add_to_cart'),
    path('add-to-cart-in-cart/<str:product_id>/', views.add_to_cart_in_cart, name='add_to_cart_in_cart'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete-from-cart/<str:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/<str:showroom_id>', views.checkout, name='checkout'),
    path('order-confirmaiton/<str:order_id>', views.complete_order, name='order_confirmaiton'),
    
    #path('order-complete/', views.order_complete, name='order_complete'),
    
    
    

]
