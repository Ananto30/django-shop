from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, ProductSKUs
from .serializers import ShowProductSerializer, CreateProductSerializer, CategorySerializer, CreateProductVariant, \
    ShowProductVariant, ShowProductSkuSerializer


class ListProductsView(generics.ListCreateAPIView):
    """
    Get all the products, saves a new product
    """
    queryset = Product.objects.all()
    serializer_class = ShowProductSerializer

    # permission_classes = (permissions.BasePermission,)

    def post(self, request, *args, **kwargs):
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSpecificProduct(generics.ListAPIView):
    """
    Get a specific product
    """
    serializer_class = ShowProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id = self.kwargs['id']
        return Product.objects.filter(id=id)


class ListCategoriesView(generics.ListCreateAPIView):
    """
    Get all the categories, saves a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListProductVariant(APIView):
#     """
#     Provides a get method handler.
#     """
#
#     def get(self, request, format=None):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = CreateProductVariant(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListProductVariant(generics.ListAPIView):
    """
    Get all product variants
    """
    queryset = ProductSKUs.objects.all()
    serializer_class = ShowProductSkuSerializer


class ListSpecificVariant(generics.ListAPIView):
    """
    Get a specific variant of a product by product uuid
    """
    serializer_class = ShowProductSkuSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        uuid = self.kwargs['uuid']
        return ProductSKUs.objects.filter(product_uuid=uuid)


class ListSpecificProductVariant(generics.ListAPIView):
    """
    Get all variants of a specific product
    """
    serializer_class = ShowProductSkuSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        id = self.kwargs['id']
        return ProductSKUs.objects.filter(product_id=id)

    # def get(self, request, format=None):
    #     product = self.get_object()
    #     product_skus = ProductSKUs.objects.filter(product_id=product)
    #     serializer = ShowProductSku(product_skus, many=True)
    #     return Response(serializer.data)
