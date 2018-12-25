from django.db import models

from product.models import Product, Detail, Supplier


# Create your models here.

class Purchase(models.Model):
    purchase_date = models.DateTimeField('Purchased at')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.FloatField()

    def __str__(self):
        return self.product_id.product_id

    def total(self):
        return self.quantity * self.purchase_price

    def save(self, *args, **kwargs):
        super(Product, self)

class Sell(models.Model):
    selling_time = models.DateTimeField('Sold at')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    selling_price = models.FloatField()

    def __str__(self):
        return self.product_id.product_id
