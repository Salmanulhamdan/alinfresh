import calendar
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import CouponForm
from coreapp.forms import OrderForm
from product.forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import get_object_or_404, render, redirect
from product.models import *
from django.forms import inlineformset_factory
from userapp.models import CustomUser
from coreapp.models import *
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay
# from .forms import AdminLoginForm

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('adminpage')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)

        if user is not None and  user.is_superuser:
            login(request,user)
            return redirect('adminpage')
        else:
            messages.error(request,"Bad credentials")
            return redirect('admin_login')
    return render(request, 'admintemplates/login.html')


@login_required(login_url='admin_login')
def adminpage(request):
    delivered_orders = Order.objects.filter(status='Delivered')
    delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
    print( delivered_orders_by_months)
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
         delivered_orders_month.append(calendar.month_name[d['delivered_month']])
         delivered_orders_number.append(list(d.values())[1])


    
    

    order_by_months = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
   

    for o in order_by_months:
        monthNumber.append(calendar.month_name[o['month']])
        totalOrders.append(list(o.values())[1])
        
    order_by_year = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')

    yearNumber = []
    total_Orders = []

    for o in order_by_year:
        yearNumber.append(o['year'])
        total_Orders.append(o['count'])   
    order_by_days = Order.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(count=Count('id')).values('day', 'count')

    dayNumber = []
    totalOrdersByDay = []

    for o in order_by_days:
        dayNumber.append(o['day'])
        totalOrdersByDay.append(o['count']) 

    context = {
        'order_by_year':order_by_year,
        'dayNumber':dayNumber,
        'monthNumber': monthNumber,
        'totalOrders': totalOrders,
        'yearNumber': yearNumber,
        'total_Orders': total_Orders,
        'delivered_orders':delivered_orders,
        'order_by_months':order_by_months,
        
        'totalOrders':totalOrders,
        'delivered_orders_number':delivered_orders_number,
        'delivered_orders_month':delivered_orders_month,
        'delivered_orders_by_months':delivered_orders_by_months,

    }

    return render(request, 'admintemplates/index.html', context)


def admin_logout(request):
    logout(request)
    messages.success(request,"Logged out succesfully")
    return redirect('admin_login')

def admin_accounts(request):
    stu = CustomUser.objects.all()
    return render(request,'admintemplates/accounts.html',{'stu':stu})
   


def user_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        user = CustomUser.objects.filter(Q(email__icontains=query) | Q(id__contains=query))

    return render(request, "admintemplates/user_search.html", {'user': user})
   


def block_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        return redirect('admin_accounts')

def unblock_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return redirect('admin_accounts')



 #admin product section

def products(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    varients=ProductVariant.objects.all()
    return render(request,'admintemplates/products.html',{'product':product,'categories':categories,'varients':varients})
   
# To add multiple images 
ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=5)
def add_products(request):
     fm= ProductForm()
     
     if request.method == "POST":
            fm= ProductForm(request.POST,request.FILES)
            image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())
            if fm.is_valid()  and image_form.is_valid():
                 product = fm.save()  # Save the product object
                 image_form.instance = product
                 image_form.save()
                #  images = request.FILES.getlist('images')
                #  for image in images:
                #     ProductImage.objects.create(product=product, image=image)
                 return redirect('products')
     else:
         fm=ProductForm()
         image_form = ProductImageFormSet(instance=Product())
     context = {
            "fm":fm,
            'image_form': image_form
        }
     return render(request,'admintemplates/add-product.html',context)
    

def delete_product(request,id):
        pi = Product.objects.get(pk=id)
        pi.delete()
        return redirect('products')
        
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('products')
    else:
        product_form = ProductForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admintemplates/edit-product.html', context)

def productbycategories(request,id):
        pdt = Product.objects.filter(category_id=id)
        return render(request,"admintemplates/categories.html",{'pdt':pdt})
       


def add_category(request):
    fm = CategoryForm()
    if request.method == 'POST':
        fm = CategoryForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('products')
        
    else:
        fm = CategoryForm()

    return render(request,'admintemplates/add_category.html',{'fm':fm})
    



#for deleting category
def delete_category(request,id):
        pi = Category.objects.get(pk=id)
        pi.delete()
        return redirect('products')


def add_variant(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            variant = form.save(commit=False)
            variant.product = product
            variant.save()
            return redirect('products')
    else:
        form = ProductVariantForm()

    return render(request, 'admintemplates/add_variant.html', {'product': product, 'form': form})



def del_product_variant(request, id):
        prod = ProductVariant.objects.get(pk=id)
        prod.delete()
        return redirect("products")


#order management


def orderpage(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, "admintemplates/order.html", {"orders": orders})

def order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    context = {
        'orders': orders,
        'myorder':myorder
    }
    return render(request, 'admintemplates/order_product.html', context)


def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
        
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
            if status=='Delivered':
                pyment=order.payment
                pyment.status='Success'
                pyment.save()


        except Order.DoesNotExist:
            pass
    return redirect("order_page")


#coupen management


def list_coupen(request):
    coupons = Coupons.objects.all()
    return render(request,'admintemplates/coupen.html',{'coupons': coupons})

def create_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_coupen')  # Redirect to a page displaying the list of coupons
    else:
        form = CouponForm()
    
    return render(request, 'admintemplates/create_coupen.html', {'form': form})

def edit_coupon(request, id):
    coupon = get_object_or_404(Coupons, pk=id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('list_coupen')  # Redirect to the coupon list page after updating the form
    else:
        form = CouponForm(instance=coupon)

    context = {'form': form}
    return render(request, 'admintemplates/create_coupen.html', context)

def delete_coupon(request, id):
    coupon = get_object_or_404(Coupons, pk=id)
    coupon.delete()
    return redirect('list_coupen')  # Redirect to the coupon list page after deleting the coupon

    




   