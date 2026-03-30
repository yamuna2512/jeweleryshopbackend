from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.Users.mixins import CustomLoginRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser
 
from .models import Category, SubCategory, Product, Cart, CartItem, Wishlist
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    WishlistSerializer
)


# =============================
# CATEGORY LIST + CREATE
# =============================
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =============================
# SUBCATEGORY LIST + CREATE
# =============================
class SubCategoryListView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


# =============================
# PRODUCT LIST + CREATE
# =============================
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    filter_backends = [filters.SearchFilter]

    search_fields = [
        "product_name",
        "description",
        "category__category_name",
        "subcategory__subcategory_name",
        "sku",
        "purity",
    ]


# =============================
# PRODUCT DETAILS
# =============================
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


# =============================
# ADD TO CART
# =============================
class AddToCartView(CustomLoginRequiredMixin, generics.GenericAPIView):
    serializer_class = CartItemSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.login_user
            product_id = request.data.get("product_id")
            quantity = int(request.data.get("quantity", 1))

            if not product_id:
                return Response({"error": "product_id is required"}, status=400)

            cart, created = Cart.objects.get_or_create(user=user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={"quantity": quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response({"message": "Item added to cart"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


# =============================
# VIEW CART ITEMS
# =============================
class CartView(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.login_user)
        return CartItem.objects.filter(cart=cart)
        # return Cart.objects.filter(user=self.request.user)


# =============================
# DELETE ITEM FROM CART
# =============================
class RemoveCartItemView(CustomLoginRequiredMixin, generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    lookup_field = "id"


# =============================
# ADD TO WISHLIST
# =============================
class AddWishlistView(CustomLoginRequiredMixin, generics.GenericAPIView):
    serializer_class = WishlistSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = request.login_user
            product_id = request.data.get("product_id")

            if not product_id:
                return Response({"error": "product_id is required"}, status=400)

            wishlist, created = Wishlist.objects.get_or_create(user=user, product_id=product_id)

            if created:
                return Response({"message": "Product added to wishlist"}, status=201)
            else:
                return Response({"message": "Product already in wishlist"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)





# =============================
# VIEW WISHLIST
# =============================
class WishlistView(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.login_user)


# =============================
# DELETE ITEM FROM WISHLIST
# =============================
class RemoveWishlistView(CustomLoginRequiredMixin, generics.DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = "id"
