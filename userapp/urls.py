from .import views
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('signout/', SignoutView.as_view(), name='signout'),
    path('otp_login/',views.otp_login,name='otp_login'),
    path('phone_very/',views.verify_code,name='phone_very'),
    path('address/create/', AddAddressView.as_view(), name='address-create'),
    path('edit_address/<int:id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:id>/', DeleteAddressView.as_view(), name='delete_address'),
    path('user-profile',views.profile,name='user_profile'),
    path('profile_address',views.profile_address,name='profile_address'),
    path('forgotPassword',views.forgotPassword,name='forgot_Password'),
    path('forgotPassword_otp',views.forgotPassword_otp,name='forgot_Password_otp'),
    path('resetPassword',views.resetPassword,name='resetPassword'),
    path('AddAddressuserView/create/', AddAddressuserView.as_view(), name='AddAddressuserView-create'),
    path('userprofileorderlist',views.userprofileorderlist,name='userprofileorderlist'),
    path('order/<int:id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:id>/return/', views.return_order, name='return_order'),
    path('myorder_details/<int:id>//', views.my_order_products, name='myorder_details'),

    path('search',views.search,name='search'),






]
