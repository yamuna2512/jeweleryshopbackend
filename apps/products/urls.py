from django.urls import path
from .views import (
    CategoryListView,
    SubCategoryListView,
    ProductListView,
    ProductDetailView,
    AddToCartView,
    CartView,
    RemoveCartItemView,
    UpdateCartItemView,
    AddWishlistView,
    WishlistView,
    RemoveWishlistView
)

urlpatterns = [
    # PRODUCTS
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:id>/", ProductDetailView.as_view(), name="product-detail"),

    # CATEGORIES
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("subcategories/", SubCategoryListView.as_view(), name="subcategory-list"),

    # CART
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("cart/update/<int:id>/", UpdateCartItemView.as_view(), name="cart-item-update"),
    path("cart/remove/<int:id>/", RemoveCartItemView.as_view(), name="cart-item-remove"),

    # WISHLIST
    path("wishlist/add/", AddWishlistView.as_view(), name="add-wishlist"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("wishlist/remove/<int:id>/", RemoveWishlistView.as_view(), name="wishlist-remove"),
]
