


from django import forms

from .models import *

from django.forms import ModelForm
from multiupload.fields import MultiFileField

# Product form
class ProductForm(ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity_in_stock', 'category', 'image',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
                     
            # 'image': forms.ClearableFileInput(attrs={'multiple': True}),
            
        }
    image = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'})



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_name','image']

# Category form
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

# # Subcategory form
# class SubcategoryForm(ModelForm):
#     class Meta:
#         model = Subcategory
#         fields = ['name', 'description', 'category']

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size', 'price', 'quantity_in_stock']