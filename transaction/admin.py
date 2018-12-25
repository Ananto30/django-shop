from django.contrib import admin

# Register your models here.

from .models import Purchase, Sell

class PurchaseList(admin.ModelAdmin):
    list_display = ('product_id', 'quantity', 'purchase_price', 'total')


admin.site.register(Purchase, PurchaseList)
admin.site.register(Sell)