import uuid

from django.db import models


def unique_id():
    return uuid.uuid4().hex.upper()[0:6]


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        primary_key=True,
        help_text="e.g. 'Fruits', 'Clothes' etc.",
    )

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(
        max_length=250,
        primary_key=True,
        help_text="'Apple', 'Banana', 'T-Shirt' etc.",
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to="products",
        help_text="Better to upload small size images",
    )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.name} - {self.category}"


class Attribute(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        primary_key=True,
        help_text="e.g. 'Color', 'Size' etc.",
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 'Kg', 'Litre' etc. It can be left blank.",
    )

    def __str__(self):
        return f"{self.name} - {self.unit}"


class AttributeValues(models.Model):
    # value_id = models.IntegerField(unique=True, primary_key=True)
    # product_id = models.ForeignKey(Product, on_delete=None)
    attribute = models.ForeignKey(Attribute, on_delete=models.RESTRICT)
    value = models.CharField(
        max_length=200,
        help_text="e.g. 'Red', 'Green', 'Small', 1, 5 etc.",
    )

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


class ProductSKUs(models.Model):
    product = models.ForeignKey(
        Product, related_name="product_skus", on_delete=models.RESTRICT
    )
    product_code = models.CharField(
        max_length=20,
        unique=True,
        default=unique_id,
        editable=False,
        help_text="Auto generated unique code",
    )

    def __str__(self):
        return f"{self.product} - {self.product_code}"


class SKUValues(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    sku = models.ForeignKey(
        ProductSKUs, related_name="sku_values", on_delete=models.RESTRICT
    )
    # attribute_id = models.ForeignKey(Attribute, on_delete=None)
    attribute_value = models.ForeignKey(AttributeValues, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.product} || {self.attribute_value}"
