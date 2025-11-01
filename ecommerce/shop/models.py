from django.db import models
from django.urls import reverse
from model_utils import FieldTracker

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})
    
    @property
    def discount_percentage(self):
        if self.original_price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - Image"

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('payment_failed', 'Payment Failed'),
        ('processing', 'Processing'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    )
    
    # Add tracker for status field
    tracker = FieldTracker(fields=['status'])
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    )
    
    SHIPPING_METHOD = (
        ('standard', 'Standard Shipping (5-7 business days)'),
        ('express', 'Express Shipping (2-3 business days)'),
        ('pickup', 'Local Pickup')
    )
    
    PAYMENT_METHOD = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking')
    )
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    
    # Financial fields
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status fields
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Tracking
    tracking_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    
    # Shipping and Payment
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_METHOD, default='standard')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='cash_on_delivery')
    
    # Additional notes
    order_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Order {self.id} - {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('shop:order_detail', kwargs={'order_id': self.id})
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'{self.product.name} - {self.order.id}'
    
    def get_total_price(self):
        return self.price * self.quantity

class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Order statuses'
    
    def __str__(self):
        return f'{self.order.tracking_number} - {self.get_status_display()}'
