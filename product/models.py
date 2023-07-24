from django.db import models

# Create your models here.
from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse


# Category model
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='No description provided')
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True ,null=True, default='')



    def get_url(self):
        return reverse('products_by_category',args= [self.slug])

    def __str__(self):
        return self.name



# Product model
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products',default='')
    created_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='name', max_length=255, unique=True ,null=True, default='')


    def get_url(self):
        return reverse('product_detail', args= [self.category.slug, self.slug])


    def __str__(self):
        return self.name
    

# product varient model  

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=200)  # e.g., '250gm', '500gm'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product.name} - {self.size}'






class ProductImage(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image",default='')
    image = models.ImageField(upload_to='products', blank=True)

    def __str__(self):
        return self.image.url



    

