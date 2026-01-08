from django.db import models
# from django.contrib.auth.models import User
from apps.Users.models import User
from cloudinary.models import CloudinaryField
# ================================
# 1. CATEGORY TABLE
# ================================
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    def __str__(self):
        return self.category_name
# ================================
# 2. SUBCATEGORY TABLE
# ================================
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=100)
    def __str__(self):
        return self.subcategory_name
# ================================
# 3. PRODUCT TABLE
# ================================
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    sku = models.CharField(max_length=50, unique=True)
    purity = models.CharField(max_length=20)        # 22K, 18K
    weight = models.DecimalField(max_digits=10, decimal_places=2)  # grams
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    product_image = CloudinaryField( null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name
# ================================
# 4. CART TABLE
# ================================
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart #{self.id} - {self.user.first_name}"
# ================================
# 5. CART ITEMS TABLE
# ================================
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
# ================================
# 6. WISHLIST TABLE
# ================================
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.first_name} → {self.product.product_name}"



