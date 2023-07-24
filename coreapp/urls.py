from . import views
from .views import CheckoutView,PlaceOrderView
from django.urls import path

urlpatterns = [
    path('thankspage/<int:order_id>/', views.thankspage, name='thankspage'),

    path('place-order-cod/<int:id>/<str:payment_method>/', PlaceOrderView.as_view(), name='place_order'),
    path('product_single/<int:id>/',views.single_page,name='product_single'),

    path('checkout/', CheckoutView.as_view(), name='checkout_view'),
    path('payment_page/<int:id>/',views.pyment_page,name='payment_page'),
    path('confirm_payment_page/<int:id>/',views.confirm_pyment_page,name='confirm_payment_page'),

    path('applycoupon',views.apply_coupon,name="apply_coupon"),
    path('apply_wallet/<int:id>/',views.apply_wallet,name="apply_wallet"),

    
    # path('order/create/', views.order_create_view, name='order-create'),

    path('',views.home,name='home'),
    path('<slug:category_slug>/', views.home, name='products_by_category'),
]