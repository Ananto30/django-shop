import uuid

from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    # id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True, upload_to='products')
    category_id = models.ForeignKey(Category, on_delete=None)

    def __str__(self):
        return "{} - {}".format(self.name, self.category_id)


class Attribute(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.unit)


class AttributeValues(models.Model):
    # value_id = models.IntegerField(unique=True, primary_key=True)
    # product_id = models.ForeignKey(Product, on_delete=None)
    attribute_id = models.ForeignKey(Attribute, on_delete=None)
    value = models.CharField(max_length=200)

    def __str__(self):
        return "{} - {}".format(self.attribute_id.name, self.value)


# if default takes a function, it will call it every time when initiated
def f():
    d = uuid.uuid4()
    string = d.hex
    return string[0:6].upper()


class ProductSKUs(models.Model):
    product_id = models.ForeignKey(Product, related_name='product_skus', on_delete=None)
    product_uuid = models.CharField(max_length=20, unique=True, default=f)

    def __str__(self):
        return "{}".format(self.product_uuid)


class SKUValues(models.Model):
    product_id = models.ForeignKey(Product, on_delete=None)
    sku_id = models.ForeignKey(ProductSKUs, related_name='sku_values', on_delete=None)
    # attribute_id = models.ForeignKey(Attribute, on_delete=None)
    value_id = models.ForeignKey(AttributeValues, on_delete=None)

    def __str__(self):
        return "{} || {}".format(self.product_id, self.value_id)
