from django.urls import path,include
from django.contrib import admin
from core import views
urlpatterns = [
    path('', views.home , name='home'),
    path('check_email', views.check_email , name='check_email'),
    path('signup', views.signup , name='signup'),
    path('logout', views.logout , name='logout'),
    
    path('user-logout/<str:showroom_id>', views.user_logout , name='user_logout'),
    
    path('showrooms/', views.showrooms , name='showrooms'),
    path('360-and-shop/360/<str:pk>', views.link_360_and_shop , name='360_and_shop'),
    path('callback', views.callback, name="callback"),
    path('360-and-shop/shop/<pk>/<id>', views.shop, name="shop"),
    path('node_visitor', views.node_visitor, name="node_visitor"),
    
    
    #dashboard
    
    path('shop-dashboard-signin', views.shop_dashboard_signin, name="shop_dashboard_signin"),
    path('dashboard_logout', views.dashboard_logout, name="dashboard_logout"),
    path('shop-dashboard', views.shop_dashboard, name="shop_dashboard"),
    path('shop-dashboard/node-info', views.node_info, name="node_info"),
    path('shop-dashboard/node-info-update', views.node_info_update, name="node_info_update"),
    path('shop-dashboard/analytics', views.google_analytics, name="google_analytics"),
    path('settings', views.settings, name="settings"),
    path('all-companies', views.all_companies, name="all_companies"),
    path('all-companies/delete-company/<str:company_id>', views.delete_company, name="delete_company"),
    path('check_company', views.check_company , name='check_company'),
    path('all-categories', views.all_categories, name="all_categories"),
    path('all-categories/delete-category/<str:category_id>', views.delete_category, name="delete_category"),
    
    path('check_category', views.check_category , name='check_category'),
    
    
    path('shop-dashboard/add-product', views.add_product, name="add_product"),
    path('shop-dashboard/all-products', views.all_products, name="all_products"),
    path('shop-dashboard/update_product/<str:id>', views.update_product, name="update_product"),
    path('shop-dashboard/delete_product/<str:id>', views.delete_product, name="delete_product"),
    
    
    
    # cart and order items
    
    path('shop-cart/<str:showroom_id>', views.shop_cart, name='shop_cart'),
    path('add-to-cart/<str:product_id>/<str:showroom_id>', views.add_to_cart, name='add_to_cart'),
    path('add-to-cart-in-cart/<str:product_id>/', views.add_to_cart_in_cart, name='add_to_cart_in_cart'),
    path('add-to-cart-in-cart-quantity/<str:product_id>/', views.add_to_cart_in_cart_quantity, name='add_to_cart_in_cart_quantity'),
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete-from-cart/<str:product_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/<str:showroom_id>', views.checkout, name='checkout'),
    path('order-confirmaiton/<str:order_id>', views.complete_order, name='order_confirmaiton'),
    
    #path('order-complete/', views.order_complete, name='order_complete'),
    
    
    path('cart-count/<str:showroom_id>', views.get_cart_count, name='get_cart_count'),
    

]
