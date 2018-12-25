from django.db import models


# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=10, unique=True, primary_key=True)
    product_name = models.CharField(max_length=250)
    product_image = models.ImageField(blank=True, null=True, upload_to='products')
    quantity = models.IntegerField(null=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.product_id

    def sell_product(self, quantity):
        self.quantity -= quantity


class Supplier(models.Model):
    supplier_id = models.CharField(max_length=10)
    supplier_name = models.CharField(max_length=250)
    supplier_address = models.CharField(max_length=250)
    supplier_phone = models.IntegerField()

    def __str__(self):
        return self.supplier_id


class Detail(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.product_id.product_id

