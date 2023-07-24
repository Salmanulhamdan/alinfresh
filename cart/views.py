from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from coreapp.models import Coupons

from userapp.models import CustomUser
from .models import Cart, Cartitem
from product.models import Product,ProductVariant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import get_object_or_404


def add_to_cart(request):
    # Fetch product_id from the request
    product_id = request.GET.get('product_id')
    print(product_id)
    product = Product.objects.get(pk=product_id)
    variant_price = request.GET.get('price')
    print(variant_price)

    if request.user.is_authenticated:
        # If the user is logged in, add the item to their cart
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Check if a variant price is selected
        if variant_price and variant_price != str(product.price):
            # Get the variant based on the selected price
            variant = ProductVariant.objects.get(product=product, price=variant_price)
            print(variant)
            cart_item, item_created = Cartitem.objects.get_or_create(user=user, Product=product, variant=variant, cart=cart)
            print(item_created)
        else:
            # If no variant is selected, add the base product to the cart
            cart_item, item_created = Cartitem.objects.get_or_create(user=user, Product=product, cart=cart)
        
        if not item_created and product.quantity_in_stock > 1:
            cart_item.quantity += 1
        cart_item.save()
        del request.session['total']
        
        return JsonResponse({"status": 200, "message": "added"})
    else:
        # If the user is not logged in, store the item in the session
        cart = request.session.get('cart', [])
        cart.append(product_id)
        
        request.session['cart'] = cart
        print(cart)
    return JsonResponse({"status": 200, "message": "added"})    


#delete from cart
def delete_from_cart(request, id):
    cart_item = Cartitem.objects.get(pk=id)
    cart_item.delete()
    
    return redirect('view_cart')
#for viewing cart
def calculate_cart_total(cart_items):
    total_price = 0

    for cart_item in cart_items:
        total_price += cart_item.sub_total

    return int(total_price)

def view_cart(request):
    if request.user.is_authenticated:
        coupons = Coupons.objects.all()
        cart = Cart.objects.filter(user=request.user).first()
        cart_items = Cartitem.objects.filter(cart=cart)
        total = calculate_cart_total(cart_items)
        if(request.session.get('total')):
            total_price=request.session.get('total')
        else:
            total_price = calculate_cart_total(cart_items)
    else:
        cart_items = []

        # Retrieve the cart items from the session
        cart_ids = request.session.get('cart', [])
        if cart_ids:
            # Fetch the cart items using the product IDs from the session
            cart_items = Cartitem.objects.filter(id__in=cart_ids)
            print

    # Calculate the subtotal for each cart item
    
    context = {
         'total':total,
        'cart_items': cart_items,
        'cart_total':total_price,
        'coupons': coupons,
        
    }
    
    return render(request, 'cart.html', context)

 # for updating item quantity

def update_cart_item_quantity(request):
     
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           cart_item = Cartitem.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            if isinstance(cart_item.variant, ProductVariant):
                if cart_item.quantity < cart_item.variant.quantity_in_stock:
                    cart_item.quantity += 1
                    

            elif isinstance(cart_item.Product, Product):
                if cart_item.quantity < cart_item.Product.quantity_in_stock:
                    cart_item.quantity += 1
                    
            
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0

        cart_item.save()

        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = Cartitem.objects.filter(cart=cart)
            total = calculate_cart_total(cart_items)
        except (Cart.DoesNotExist):
            return JsonResponse({'status': 404, 'error': 'Cart not found'})
       
        if 'total' in request.session:
            del request.session['total'] 
       
  

        return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal': cart_item.sub_total ,'total':total})
        
    


    


