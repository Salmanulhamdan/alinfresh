from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from cart.models import Cartitem
from product.models import Product, ProductVariant
from .forms import *
from datetime import datetime
from .models import CustomUser, CustomUserManager , Address,Wallet
from .import helper
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from coreapp .models import Order, OrderProduct, Return
from django.db.models import Q
from django.utils import timezone
import uuid
import decimal

#user signup and user login
class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                phone_number=form.cleaned_data['phone_number'],
               
            )
            
            login(request, user)
            request.session['username'] = user.username
            return redirect('home')
        return render(request, 'signup.html', {'form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password) 
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                return redirect('home')
            else:
                form.add_error(None, 'Invalid credentials')
        return render(request, 'login.html', {'form': form})

class SignoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        
        return redirect('home')
    

#otp-login

    
def verify_code(request):
    if request.user.is_authenticated:
            return redirect("home")
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone') 
            if helper.check(phone_no, code):                
                user = CustomUser.objects.get(email = request.session.get('username'))
                userobj = CustomUser.objects.filter(email = request.session.get('username'))
                if userobj is not None and user.is_active and user.is_superuser == False:
                    login(request, user)
                    return redirect('home')
              
                return redirect('home')
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'otp.html', {'form': form})


def otp_login(request):
    if request.user.is_authenticated:
            return redirect("home")
    if request.method == "POST":
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(request.POST['phone_number']):           
            user = username_password(request.POST['phone_number'])
            if user is not None:
                helper.send(phone)
                request.session['username'] = user.email
                user.is_verified = True
                user.is_active = True
                request.session['phone'] = phone
                return redirect('phone_very')
            else:
                context = "Please register first"
                return render(request, 'register.html',{'context':context})
    return render(request, 'register.html')

def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
  
    return user

def check_phone_number(phone_number):
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number)
        
        return True
    except CustomUser.DoesNotExist:
        return False
 #otp-login-end   

#for adding shipping address
class AddAddressView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('checkout_view')  


#foe editing the address
def edit_address(request, id):
    # Fetch the address object from the database using the address_id
    address = get_object_or_404(Address, pk=id)

    if request.method == 'POST':
        # If the form was submitted, process the data
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('profile_address')  # Replace 'address_list' with the URL name of the address list view
    else:
        # If the request method is GET, display the form with the current data
        form = AddressForm(instance=address)

    return render(request, 'address.html', {'form': form})

#for deleting address

class DeleteAddressView(View):
    def get(self, request, id):
        prod = Address.objects.get(pk=id)
        prod.delete()
        return redirect('checkout_view')
    

User = get_user_model()

@login_required
def profile(request):
    user = request.user
    # orders = Order.objects.filter(user=user)

    # Get the user's address
    address = Address.objects.filter(user=user)
    try:
        user_wallet = Wallet.objects.get(user=request.user)
        if user_wallet.balance==0:
             user_wallet=None
             
    except Wallet.DoesNotExist:
        user_wallet = None

    context = {
        'user': user,
        # 'orders': orders,
        'address': address,
        'wallet':user_wallet
    }

    return render(request, 'user.html', context)

def profile_address(request):
    user = request.user
    # orders = Order.objects.filter(user=user)

    # Get the user's address
    address = Address.objects.filter(user=user)

    context = {
        'user': user,
        # 'orders': orders,
        'address': address
    }

    return render(request, 'user_address.html', context)




#forgot password

def forgotPassword(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        
        # checking the null case
        if mobile_number_forgotPassword == '':
            # messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        
        
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
            
        if user:  #if user exists
            helper.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgot_Password_otp')
        else:
            # messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgot_Password')
            
    return render(request, 'register.html')



def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
          
        form = VerifyForm(request.POST)
        if form.is_valid():
             otp  = form.cleaned_data.get('code')
        if helper.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                return redirect('resetPassword')
        else:
            # messages.warning(request,'Invalid OTP')
            return redirect('forgot_Password_otp')
    else:
        form = VerifyForm()

        
    return render(request, 'otp.html', {'form': form})




def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')    
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)         
            user.set_password(password1)
            user.save()
            # messages.success(request, 'Password changed successfully')
            return redirect('login')
        else:
            # messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'resetpassword.html')




class AddAddressuserView(CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile_address')  
    



@login_required(login_url='signin')
def userprofileorderlist(request):
  
    order = Order.objects.filter(user=request.user).order_by("-created_at")

    context = {
        'orders': order,
    }
    return render(request, 'myorders.html', context)

#order cancel function

def cancel_order(request,id):
    
    if request.method == "POST":
        cancellation_reason = request.POST.get('cancellation_reason')
        try:
        
            order = get_object_or_404(Order, pk=id, user=request.user)
            order.status = 'Cancelled'
            order.cancellation_reason = cancellation_reason
            order.save()
            products=OrderProduct.objects.filter(order=order)
            for item in products:
                if isinstance(item.variation, ProductVariant):
                    variant = item.variation
                    variant.quantity_in_stock += item.quantity
                    variant.save()
                elif isinstance(item.product, Product):
                    product = item.product
                    product.quantity_in_stock += item.quantity
                    product.save()
            if order.payment.payment_method =='Online':
                wallet, _ =Wallet.objects.get_or_create(user=request.user)
                refund_amount=decimal.Decimal(order.order_total)
                wallet.balance += refund_amount
                wallet.save()

        except Order.DoesNotExist:
            pass
    return redirect("userprofileorderlist")


#order return function

def return_order(request,id):
   
    if request.method=="POST":
        return_reason=request.POST.get('return_reason')
        try:
            order=get_object_or_404(Order,pk=id,user= request.user)
            order.status='Returned'
            order.save()
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().fields[-1])[:8]
            tracking_number=f'{timestamp}-{unique_id}'
            order_return=Return.objects.create(order=order,return_reason=return_reason,tracking_number=tracking_number)
            order_return.save()
        except Order.DoesNotExist:
            pass
    return redirect('userprofileorderlist')






#for searching in home page
def search(request):
    if "keyword" in request.GET:
        keyword=request.GET['keyword']
     
    
        products=Product.objects.order_by('created_at').filter(Q(name_icontains=keyword) | Q(description_icontains=keyword) )
        product_count=products.count()
        context={
            'products':products,
            'product_count':product_count,
        }
        return render(request,'index.html',context)
    else:
        return render (request,'index.html')
    


def my_order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    context = {
        'orders': orders,
        'myorder':myorder
    }
    return render(request, 'my_order_detail.html', context)
    



   