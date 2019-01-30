from django.urls import path
from .views import ListProductsView, ListCategoriesView, ListProductVariant, ListSpecificProduct, ListSpecificProductVariant, ListSpecificVariant

urlpatterns = [
    path('', ListProductsView.as_view(), name="products-all"),
    path('<int:id>', ListSpecificProduct.as_view(), name="product"),
    path('<int:id>/variants', ListSpecificProductVariant.as_view(), name="product-variants-all"),

    path('categories', ListCategoriesView.as_view(), name="categories-all"),
    # path('<int:id>/categories', ),

    path('variants', ListProductVariant.as_view(), name="variants-all"),
    path('variants/<str:uuid>', ListSpecificVariant.as_view(), name="product-variant"),

]
