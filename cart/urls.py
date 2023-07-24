from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:id>/', views.delete_from_cart, name='delete_from_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart_item_quantity/', views.update_cart_item_quantity, name='update_cart_item_quantity'),
    
]
