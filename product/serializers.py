import json

from rest_framework import serializers
from .models import Product, Category, Attribute, AttributeValues, ProductSKUs, SKUValues


class ShowProductSerializer(serializers.ModelSerializer):
    product_skus = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        # fields = ("name", "image", "category_id")
        # exclude = ("id",)
        fields = '__all__'
        depth = 1


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = ("name", "image", "category_id")
        # exclude = ("id",)
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CreateAttribute(serializers.ModelSerializer):
    class Meta:
        model = Attribute


class AddAttributeValues(serializers.ModelSerializer):
    class Meta:
        model = AttributeValues


class CreateProductVariant(serializers.ModelSerializer):
    attributes = CreateAttribute(many=True)
    attribute_values = AddAttributeValues(many=True)

    class Meta:
        model = ProductSKUs
        fields = ('product_id', 'attributes', 'attribute_values')


class ShowSkuValues(serializers.ModelSerializer):
    class Meta:
        model = SKUValues
        fields = ('value_id',)
        depth = 2


class ShowProductSkuSerializer(serializers.ModelSerializer):
    # sku_values = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sku_values = ShowSkuValues(many=True, read_only=True)

    class Meta:
        model = ProductSKUs
        fields = ('product_id', 'product_uuid', 'sku_values')
        depth = 1


class ShowProductVariant(serializers.Serializer):
    # sku_values = ShowSkuValues(many=True)
    product_sku = ShowProductSkuSerializer(many=True)

# class CreateProductVariant(serializers.Serializer):
#     name = serializers.CharField(required=True)
#     category = serializers.PrimaryKeyRelatedField(required=True, )
