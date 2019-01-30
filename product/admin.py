from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from .models import Product, Category, Attribute, ProductSKUs, AttributeValues, SKUValues
from transaction.models import Purchase


# Register your models here.

# class SupplierAdmin(admin.TabularInline):
#     model = Supplier
#
#
class SKUValuesAdmin(admin.StackedInline):
    model = SKUValues
    extra = 1


class ProductSKUsAdmin(admin.ModelAdmin):
    inlines = [
        SKUValuesAdmin,
    ]

    list_display = ('product_id', 'product_uuid')


class ProductAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     ('Product Information', {'fields': ('name', 'category_id')}),
    # )
    list_display = ('name', 'id', 'category_name')
    search_fields = ('id', 'name')

    def category_name(self, obj):
        return obj.category_id.name


# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         PurchaseAdmin,
#     ]
#     list_display = ('product_name', 'product_id', 'quantity')
#     search_fields = ('product_id', 'product_name')
#
#     def quantity(self, obj):
#         purchases = obj.purchase_set.all()
#         quantity = 0
#         for purchase in purchases:
#             if str(purchase.product_id) == str(obj.product_id):
#                 quantity = quantity + purchase.quantity
#
#         return quantity
#
#     # def supplier_name(self, obj):
#     #     return obj.supplier_id.supplier_name


class LogEntryAdmin(admin.ModelAdmin):
    list_display_links = None
    list_display = ('__str__', 'get_edited_object', 'object_id', 'action_time', 'user', 'content_type',
                    'show_url')

    def show_url(self, obj):
        url = reverse('admin:{}_{}_change'.format(obj.content_type.app_label, obj.content_type.model),
                      args=(obj.object_id,))
        return format_html("<a href='{}'>See {}</a>", url, obj.object_id)

    show_url.allow_tags = True

    def has_add_permission(self, request, obj=None):
        return False


class SupplierAdmin(admin.ModelAdmin):
    exclude = None


# models = [Product, Supplier]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValues)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(ProductSKUs, ProductSKUsAdmin)
