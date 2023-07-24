from django.contrib import admin

from alinfresh.settings import AUTH_USER_MODEL


from .models import Product, Category,ProductVariant,ProductImage

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')


class ProductVariantAdmin(admin.ModelAdmin):
    list_display=('product','quantity_in_stock',)
    


class ProductAdmin(admin.ModelAdmin):
    list_display=('name','slug','id','quantity_in_stock')
    


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)

admin.site.register(ProductVariant,ProductVariantAdmin)

admin.site.register(ProductImage)


# from django.contrib import admin


#admin.site.register(Subcategory)
