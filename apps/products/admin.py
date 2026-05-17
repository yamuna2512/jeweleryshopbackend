from django.contrib import admin
from .models import Category, SubCategory, Product, Cart, CartItem, Wishlist, Order, OrderItem

# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")
    search_fields = ("category_name",)


# admin.site.register(SubCategory)
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "subcategory_name", "category")
    list_filter = ("category",)
    search_fields = ("subcategory_name",)

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "category", "subcategory", "purity", "price", "stock", "product_image")
    list_filter = ("category", "subcategory", "purity")
    search_fields = ("product_name", "sku")
    ordering = ("-created_at",)



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_id", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)

    # Show user ID
    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = "User ID"


class UserIDFilter(admin.SimpleListFilter):
    title = "User ID"
    parameter_name = "user_id"

    def lookups(self, request, model_admin):
        # Get distinct user IDs from CartItem
        user_ids = CartItem.objects.values_list('cart__user_id', flat=True).distinct()
        return [(uid, str(uid)) for uid in user_ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cart__user_id=self.value())
        return queryset

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "get_cart_display", "get_product_id", "quantity")
    # list_filter = ("user_id",)
    list_filter = (UserIDFilter,) 

    search_fields = ("product__id", "cart__user__email")

    def get_product_id(self, obj):
        return obj.product.id
    get_product_id.short_description = "Product ID"

    def get_cart_display(self, obj):
        return f"Cart #{obj.cart.id} - User {obj.cart.user.id}"
    get_cart_display.short_description = "Cart"


class WishlistUserIDFilter(admin.SimpleListFilter):
    title = "User ID"
    parameter_name = "user_id"

    def lookups(self, request, model_admin):
        user_ids = Wishlist.objects.values_list("user_id", flat=True).distinct()
        return [(uid, str(uid)) for uid in user_ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id=self.value())   # IMPORTANT
        return queryset


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "get_user_id", "get_product_id")
    list_filter = (WishlistUserIDFilter,)     # ← USE CORRECT FILTER HERE
    search_fields = ("user__email", "product__id")

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = "User ID"

    def get_product_id(self, obj):
        return obj.product.id
    get_product_id.short_description = "Product ID"

class OrderUserIDFilter(admin.SimpleListFilter):
    title = "User ID"
    parameter_name = "user_id"

    def lookups(self, request, model_admin):
        user_ids = Order.objects.values_list("user_id", flat=True).distinct()
        return [(uid, str(uid)) for uid in user_ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "get_user_id",
        "customer_name",
        "customer_phone",
        "city",
        "state",
        "total_price",
        "total_qty",
        "status",
        "created_at"
    )

    list_filter = (
        OrderUserIDFilter,
        "status",
        "city",
        "state",
    )

    search_fields = (
        "customer_name",
        "customer_phone",
        "user__email",
    )

    ordering = ("-created_at",)

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = "User ID"

# @admin.register(OrderItem)

class OrderItemUserIDFilter(admin.SimpleListFilter):
    title = "User ID"
    parameter_name = "user_id"

    def lookups(self, request, model_admin):
        user_ids = OrderItem.objects.values_list(
            "order__user_id",
            flat=True
        ).distinct()

        return [(uid, str(uid)) for uid in user_ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(order__user_id=self.value())
        return queryset


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "get_order_id",
        "get_user_id",
        "get_product_id",
        "quantity",
        "price",
        "created_at"
    )

    list_filter = (OrderItemUserIDFilter,)

    search_fields = (
        "order__customer_name",
        "product__product_name",
    )

    ordering = ("-created_at",)

    def get_order_id(self, obj):
        return obj.order.id
    get_order_id.short_description = "Order ID"

    def get_user_id(self, obj):
        return obj.order.user.id
    get_user_id.short_description = "User ID"

    def get_product_id(self, obj):
        return obj.product.id
    get_product_id.short_description = "Product ID"

