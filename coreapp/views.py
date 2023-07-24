
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from urllib3 import HTTPResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from product.models import*
from cart.models import Cartitem,Cart
from userapp.models import Address, Wallet
from django.views import View
from .models import *
from .forms import *
from django.views.generic import CreateView,TemplateView
import razorpay
from datetime import date
import json
import uuid
from django.utils import timezone
import decimal


# Create your views here.

#function for showing home page
def home(request,category_slug=None):
       # view to set url for different categories
    
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug= category_slug)
        products = Product.objects.filter(category= categories)
        
    else:
        # saving all the items from products to list it in a dictionary
        products = Product.objects.all()
        categories = Category.objects.all()     
        
    
    context = {
        'product': products,
  
    }
    return render(request,'index.html',context)
   
#  for showing single_page

def single_page(request, id):
    product = Product.objects.get(pk=id)
    # categories = Category.objects.get(pk=id)
    variants = product.productvariant_set.all()
    return render(request,'single.html',{'product':product,'variants': variants})

#function for calculating total price in a cart
def calculate_cart_total(cart_items):
    total_price = 0

    for cart_item in cart_items:
        total_price += cart_item.sub_total

    return int(total_price)



#view for showing chekout_view
class CheckoutView(View):

    def get(self, request):
        cart=Cart.objects.get(user=request.user)
        cart_items = Cartitem.objects.filter(user=request.user)
      
        if(request.session.get('total')):
            total_price=request.session.get('total')
        else:
            total_price = calculate_cart_total(cart_items)
        address = Address.objects.filter(user=request.user)
        count=cart_items.count()

        context = {
            
            'cart_items': cart_items,
            'cart_total': total_price,
            'address': address,
            'count':count
        
        }

        return render(request, 'checkout.html', context)
    

def pyment_page(request,id):
    address=Address.objects.get(id=id)
    cart_items = Cartitem.objects.filter(user=request.user)
    try:
        user_wallet = Wallet.objects.get(user=request.user)
        if user_wallet.balance==0:
             user_wallet=None
             
    except Wallet.DoesNotExist:
        user_wallet = None
   
    if(request.session.get('total')):
            total_price=request.session.get('total')
    else:
            total_price = calculate_cart_total(cart_items)
 

  
    print(total_price)
    

    context={
        'address':address,
        'cart_items': cart_items,
        'total':total_price,
        'wallet':user_wallet
     
    }

    return render(request, 'payment.html',context)

def confirm_pyment_page(request,id):
    address=Address.objects.get(id=id)
    cart_items = Cartitem.objects.filter(user=request.user)
    if(request.session.get('total')):
            total_price=request.session.get('total')
    else:
            total_price = calculate_cart_total(cart_items)
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    # print(client)
    # data = { "amount": total_price, "currency": "INR", "receipt": "order_rcptid_11" }
    print(total_price)
    payment = client.order.create({ "amount": total_price*100, "currency": "INR", "receipt": "order_rcptid_11" })

    context={
        'address':address,
        'cart_items': cart_items,
        'total':total_price,
        'payment':payment,
    }

    return render(request, 'confirm_pyment.html',context)
    
    

#view for order


class PlaceOrderView(View):

    def get(self, request, id,payment_method):
        # Retrieve user, address, and other necessary data from the request
        user = request.user
        address = Address.objects.get(id=id)
        payment_method = payment_method  
        status=''
        if payment_method=='Online':
            status='Success'
        else:
            status='Pending'

        # Retrieve the user's cart or order items
        cart_items = Cartitem.objects.filter(user=request.user)
        if(request.session.get('total')):
            total_price=request.session.get('total')
        else:
            total_price = calculate_cart_total(cart_items)
        # Create a new payment entry
        payment = Payment.objects.create(
            user=user,
            payment_method=payment_method,
            amount_paid=total_price, 
            status=status  # Set initial status to Pending
        )

        # Create a new order
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().fields[-1])[:8]
        order_number = f'{timestamp}-{unique_id}'
        order = Order.objects.create(
            user=user,
            payment=payment,
            address=address,
            order_number=order_number,  
            order_note='',  
            order_total=total_price,  
            tax=0.0,  
            status='New',  
            ip='...', 
            is_ordered=False  
        )

        # Create OrderProduct instances for each cart item and update the order total
        for cart_item in cart_items:
            if isinstance(cart_item.variant, ProductVariant):
                product_price=cart_item.variant.price
            elif isinstance(cart_item.Product, Product):
                product_price=cart_item.Product.price
            OrderProduct.objects.create(
                order=order,
                payment=payment,
                user=user,
                product=cart_item.Product,
                variation=cart_item.variant,
                quantity=cart_item.quantity,
                
                                    #create condition for adding product varient price
                product_price=product_price,
                ordered=False
            )
          
            order.save()
            if isinstance(cart_item.variant, ProductVariant):
                variant = cart_item.variant
                variant.quantity_in_stock -= cart_item.quantity
                variant.save()
            elif isinstance(cart_item.Product, Product):
                product = cart_item.Product
                product.quantity_in_stock -= cart_item.quantity
                product.save()
            

        # Clear the user's cart or order items
        cart_items.delete()
        if 'total' in request.session:
            del request.session['total']

        # Redirect to a success page or show a success message
        thankspage_url = reverse('thankspage', args=[order.id])
        print(order.id)
        print(thankspage_url)
        return redirect(thankspage_url)
                                 
def thankspage(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'order': order}
    return render(request, 'thanks.html', context)

# coupen applying

@require_POST
def apply_coupon(request):
    if(request.session.get('total')):
        body = json.loads(request.body)
        grand_total = request.session.get('total')
        coupon_code = body['coupon']
        coupon = Coupons.objects.get(code__iexact=coupon_code)
        discount=int(coupon.discount)

        data={
             'discount':discount,
             "total": grand_total,
           "message":"you applied one coupen"
       }
        return JsonResponse(data)
    else:
        body = json.loads(request.body)
        grand_total = int(body['grand_total'])
        coupon_code = body['coupon']
        try:
            coupon = Coupons.objects.get(code__iexact=coupon_code)
        except Coupons.DoesNotExist:
            data = {
                "total": grand_total,
                "message": "Not a Valid Coupon"
            }
        else:
            today = date.today()
            valid_from = coupon.valid_from.date()
            valid_to = coupon.valid_to.date()
            discount=int(coupon.discount)
            min_amount = int(coupon.min_amount)
            if min_amount < grand_total and valid_from <= today <= valid_to:
                grand_total = grand_total - discount
                request.session['total'] = grand_total  # Update the session variable
                request.session['discount']=discount
                data = {
                    'discount':discount,
                    "total": grand_total,
                    "message": f"{coupon.code} Applied"
                }
            else:
                data = {
                    
                    "total": grand_total,
                    "message": "Not a Valid Coupon"
                }
        return JsonResponse(data)







def apply_wallet(request,id):
    user = request.user
    cart_items = Cartitem.objects.filter(user=user)
    if(request.session.get('total')):
            total_price=(request.session.get('total'))
    else:
            total_price = calculate_cart_total(cart_items)
    address=Address.objects.get(id=id)
    
    wallet = Wallet.objects.get(user=user)
    
    max_reduction = wallet.apply_wallet_amount(total_price)
 

    if max_reduction:
         total_price -= max_reduction
    request.session['total'] = total_price
    
   
    context = {
        'address':address,
        'cart_items': cart_items,
        'total': total_price,
        'max_reduction': max_reduction,
    }
    return render(request, 'payment.html', context)
    





