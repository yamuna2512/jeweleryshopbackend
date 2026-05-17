from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.Users.mixins import CustomLoginRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser
 
from .models import Category, SubCategory, Product, Cart, CartItem, Wishlist,OrderItem, Order
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    WishlistSerializer,
    OrderSerializer,
    OrderItemSerializer,

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
# UPDATE CART ITEM
# =============================
class UpdateCartItemView(CustomLoginRequiredMixin, generics.UpdateAPIView):
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


# =============================
# create order 
# =============================
class CreateOrderView(CustomLoginRequiredMixin, generics.GenericAPIView):

    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):

        try:
            user = request.login_user

            cart, created = Cart.objects.get_or_create(user=user)

            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                return Response(
                    {"error": "Cart is empty"},
                    status=400
                )

            total_price = 0
            total_qty = 0

            # CALCULATE TOTAL
            for item in cart_items:

                total_price += item.product.price * item.quantity

                total_qty += item.quantity

            # CREATE ORDER
            order = Order.objects.create(
                user=user,
                customer_name=request.data.get("customer_name"),
                customer_phone=request.data.get("customer_phone"),
                address=request.data.get("address"),
                pin_code=request.data.get("pin_code"),
                building_type=request.data.get("building_type"),
                city=request.data.get("city"),
                state=request.data.get("state"),
                total_price=total_price,
                total_qty=total_qty,
            )

            # CREATE ORDER ITEMS
            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # REDUCE STOCK
                product = item.product
                product.stock -= item.quantity
                product.save()

            # CLEAR CART
            cart_items.delete()

            serializer = OrderSerializer(order)

            return Response(
                {
                    "message": "Order placed successfully",
                    "data": serializer.data
                },
                status=201
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400
            )
        
# =============================
# view order 
# =============================
class MyOrdersView(CustomLoginRequiredMixin, generics.ListAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.login_user
        ).order_by("-id")    
    
# =============================
# order details
# =============================
class OrderDetailView(CustomLoginRequiredMixin, generics.RetrieveAPIView):

    serializer_class = OrderSerializer
    lookup_field = "id"

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.login_user
        )
    

# =============================
# cncel order 
# =============================
class CancelOrderView(CustomLoginRequiredMixin, generics.UpdateAPIView):

    serializer_class = OrderSerializer
    lookup_field = "id"

    def get_queryset(self):

        return Order.objects.filter(
            user=self.request.login_user
        )

    def update(self, request, *args, **kwargs):

        order = self.get_object()

        if order.status == "Cancelled":
            return Response(
                {"message": "Order already cancelled"},
                status=400
            )

        order.status = "Cancelled"
        order.save()

        return Response(
            {"message": "Order cancelled successfully"},
            status=200
        )