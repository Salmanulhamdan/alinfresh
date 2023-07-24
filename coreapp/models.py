from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from product.models import *
from userapp.models import Address

# Create your models here.



User = get_user_model()

class Payment(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method}--{self.status}"
    
class Order(models.Model):
    

    user    = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True,default='') 
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=50,null=True)
    order_note = models.CharField(max_length=50, blank=True)
    order_total = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=50,default='New')
    cancellation_reason = models.TextField(blank=True)
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="myorders")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user}-{self.product} - {self.quantity}"


#model for return orders

class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    return_reason = models.TextField()
    tracking_number = models.CharField(max_length=255)
    return_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    # Add any other relevant fields

    def __str__(self):
        return f"Reason for return {self.return_reason}"



#cmodel for creating coupens

class Coupons(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    min_amount  = models.IntegerField()
    active  = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

