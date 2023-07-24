from django.db import models
from django.contrib.auth import get_user_model
from product.models import *
# Create your models here.



User=get_user_model()

# Create your models here.
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
  
    
class Cartitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='cart_items')
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    @property
    def sub_total(self):
        if self.variant:
            return self.variant.price * self.quantity
        else:
            return self.Product.price * self.quantity

    def __str__(self):
        return str(self.user.name ) + "--" + str(self.Product)
