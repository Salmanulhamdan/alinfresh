from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('edit_order/<int:id>/',views.edit_order,name='edit_order'),

    path('',views.admin_login, name='admin_login'),
    path('adminpage',views.adminpage,name='adminpage'),
    path('adminlogout',views.admin_logout,name='adminlogout'),
    path('products',views.products,name='products'),
    path('admin_accounts',views.admin_accounts,name='admin_accounts'),
    path('user_search',views.user_search,name='user_search'),
    path('block_user/<int:id>/', views.block_user,name="block_user"),
    path('unblock_user/<int:id>/', views.unblock_user,name="unblock_user"),
    path('add_products',views.add_products,name='add_products'),
    path('add_category',views.add_category,name='add_category'),
    path('productbycategories/<int:id>/',views.productbycategories,name='productbycategories'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
    path('add_varient/<int:id>/',views.add_variant,name='varient'),
    path('delete_varient/<int:id>/',views.del_product_variant,name='delete_varient'),
    path('order_management',views.orderpage,name="order_page"),
    path('edit_order/<int:id>/',views.edit_order,name='edit_order'),
    path('list_coupen',views.list_coupen,name="list_coupen"),
    path('sales_date',views.sales_date,name="sales_date"),
    path('create_coupen',views.create_coupon,name="create_list_coupen"),
    path('edit_coupon/<int:id>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),

    path('order_product/<int:id>/',views.order_products,name="order_product"),
   
]



