import uuid
from django.forms import ValidationError
from django.db import models
import datetime
from django.utils.timezone import now
from product.models import Product, ProductSKUs


# Create your models here.


class Supplier(models.Model):
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    phone = models.IntegerField()

    def __str__(self):
        return self.id


class Purchase(models.Model):
    date = models.DateTimeField('Purchased at', default=now)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.date.strftime("%d-%m-%Y %I:%M %p")
    #
    # def total(self):
    #     return self.quantity * self.purchase_price


class PurchaseProduct(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.SET_NULL, null=True)
    product_uuid = models.CharField(max_length=20)
    quantity = models.IntegerField(null=False)
    sold_quantity = models.IntegerField(default=0)
    purchase_price_per_unit = models.FloatField()
    sale_price_per_unit = models.FloatField()

    def __str__(self):
        return self.product_uuid


class Sale(models.Model):
    date = models.DateTimeField('Sold at', default=now)
    discount = models.FloatField(default=0.0)

    class Meta:
        permissions = (
            ('read_item', 'Can read item'),
        )

    @property
    def items(self):
        products = self.saleproduct_set.all()
        return ', '.join([p.product_uuid for p in products])


class SaleProduct(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    product_uuid = models.CharField(max_length=20)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return self.product_uuid

    def clean(self, *args, **kwargs):
        try:
            product = PurchaseProduct.objects.get(product_uuid=self.product_uuid)
            print(self.quantity)
            if self.quantity > product.quantity:
                raise ValidationError(
                    "You have '{}' item(s) left. But want to sell '{}'.".format(
                        (product.quantity - product.sold_quantity), self.quantity))
            product.sold_quantity = product.sold_quantity + self.quantity
            product.save()
        except PurchaseProduct.DoesNotExist:
            raise ValidationError(
                "Product '{}' does not exist.".format(self.product_uuid))
        except Exception as e:
            raise ValidationError(e)
        super(SaleProduct, self).clean(*args, **kwargs)

# class Sell(models.Model):
#     selling_time = models.DateTimeField('Sold at')
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     supplier_id = ChainedForeignKey(Supplier,
#                                     chained_field="product_id",
#                                     chained_model_field="purchase_id")
#     quantity = models.IntegerField(null=False)
#     selling_price = models.FloatField()
#
#     def __str__(self):
#         return self.product_id.product_id
#
#     def total(self):
#         return self.quantity * self.selling_price
#
#     def profit(self):
#         return self
#
#     def get_product(self):
#         product = Product.objects.get(product_id=self.product_id)
#         return product
#
#     def purchase_id(self):
#         purchase = Purchase.objects.get(product_id=self.product_id)
#         return purchase.id
#
#     # custom validation
#     def clean(self, *args, **kwargs):
#         try:
#             product = Purchase.objects.get(product_id=self.product_id, supplier_id=self.supplier_id)
#             print(self.quantity)
#             if self.quantity > product.quantity:
#                 raise ValidationError(
#                     "You have '{}' item(s) left. But want to sell '{}'.".format(product.quantity, self.quantity))
#             product.quantity = product.quantity - self.quantity
#             product.save()
#         except Purchase.DoesNotExist:
#             raise ValidationError(
#                 "Product '{}' does not have '{}' supplier.".format(self.product_id.product_name, self.supplier_id))
#         except Exception as e:
#             raise ValidationError(e)
#         super(Sell, self).clean(*args, **kwargs)
#
#     def save(self, *args, **kwargs):
#         # calling the custom validation
#         # self.full_clean()
#         super(Sell, self).save(*args, **kwargs)
