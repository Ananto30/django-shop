import csv

from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse

from product.models import Product

from .models import Purchase, PurchaseProduct, Sale, SaleProduct, Supplier


class PurchaseProductAdminInline(admin.TabularInline):
    exclude = ["sold_quantity"]
    model = PurchaseProduct
    extra = 1

    list_display = ("quantity", "product_code")


class PurchaseAdmin(admin.ModelAdmin):
    # list_display = ('id', 'quantity', 'purchase_price', 'total')

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.annotate(
    #         _total=Count("hero", distinct=True),
    #         _villain_count=Count("villain", distinct=True),
    #     )
    #     return queryset
    inlines = [
        PurchaseProductAdminInline,
    ]
    list_display = ("date", "supplier_name")

    def supplier_name(self, obj):
        return obj.supplier_id.name


class PurchaseProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_code",
        "quantity",
        "sold_quantity",
        "purchase_price_per_unit",
        "sale_price_per_unit",
    )


class SaleProductAdminInline(admin.StackedInline):
    model = SaleProduct
    extra = 1


class SaleAdmin(admin.ModelAdmin):
    inlines = [
        SaleProductAdminInline,
    ]
    exclude = ["sold_quantity"]

    list_display = ("date", "items")

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm("sale.read_item"):
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj=obj)


class SaleProductAdmin(admin.ModelAdmin):
    date_hierarchy = "sale_id__date"
    list_display = ("sold_at", "product_code", "quantity")
    list_filter = (("sale_id__date", DateFieldListFilter),)
    search_fields = ("product_code",)

    def sold_at(self, obj):
        return obj.sale_id.date


class SellAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    list_display_links = None
    date_hierarchy = "selling_time"

    list_display = (
        "product",
        "product_name",
        "quantity",
        "selling_price",
        "total",
        "selling_time",
        "supplier_id",
    )
    list_filter = ("product_id", ("selling_time"))
    search_fields = ("product_id", "selling_time")

    def product_name(self, obj):
        return obj.product_id.product_name

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export as CSV"

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "supplier_name":
            kwargs["queryset"] = Supplier.objects.filter(name="Test")
        return super(SellAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(PurchaseProduct, PurchaseProductAdmin)
admin.site.register(Supplier)
