from django.contrib import admin

# Register your models here.

from .models import Product, Detail, Supplier
from transaction.models import Purchase


# class SupplierAdmin(admin.TabularInline):
#     model = Supplier
#
#
# class PurchaseAdmin(admin.TabularInline):
#     model = Purchase
#
#
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         PurchaseAdmin,
#         # SupplierAdmin,
#     ]
#     # list_display = ('product_name', 'product_id', 'quantity', 'supplier_name')
#     search_fields = ('product_id', 'product_name')
#
#     # def get_quantity(self, obj):
#     #     return obj.product_id.quantity
#
#     def sell(self):
#         return Product.sell_product()

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_id', 'quantity',)
    search_fields = ('product_id', 'product_name')



models = [Product, Supplier]
admin.site.register(Product, ProductAdmin)
