

from rest_framework import serializers
from django.conf import settings
from .models import Category, SubCategory, Product, Cart, CartItem, Wishlist

# ==================================
# CATEGORY SERIALIZER
# ==================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# ==================================
# SUBCATEGORY SERIALIZER
# ==================================
class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )

    class Meta:
        model = SubCategory
        fields = ["id", "subcategory_name", "category", "category_name"]


# ==================================
#  PRODUCT SERIALIZER (FIXED)
# ==================================
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )
    subcategory_name = serializers.CharField(
        source="subcategory.subcategory_name", read_only=True
    )

    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "description",
            "sku",
            "purity",
            "weight",
            "price",
            "stock",
            "product_image",
            "category",
            "subcategory",
            "category_name",
            "subcategory_name",
            "created_at",
        ]

    def get_product_image(self, obj):
        if obj.product_image:
            return obj.product_image.url
        return None

# ==================================
# CART ITEM SERIALIZER
# ==================================
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


# ==================================
# CART SERIALIZER
# ==================================
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "items"]


# ==================================
# WISHLIST SERIALIZER
# ==================================
class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "product"]
