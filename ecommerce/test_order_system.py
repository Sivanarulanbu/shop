
import os
import django
import uuid
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import Product, Order, OrderItem, Category, Brand, OrderStatus
from django.contrib.auth.models import User
from django.utils import timezone

def run_test():
    print("Starting Order System Test...")
    
    # 1. Get or create a user
    user, _ = User.objects.get_or_create(username='testuser', email='test@example.com')
    print(f"User: {user.username}")
    
    # 2. Get or create category and brand
    cat, _ = Category.objects.get_or_create(name='Test Category', slug='test-category')
    brand, _ = Brand.objects.get_or_create(name='Test Brand', slug='test-brand')
    
    # 3. Create a product if none exists
    product, created = Product.objects.get_or_create(
        name='Test Product',
        defaults={
            'slug': f'test-product-{uuid.uuid4().hex[:6]}',
            'price': Decimal('99.99'),
            'category': cat,
            'brand': brand,
            'stock': 10,
            'available': True
        }
    )
    print(f"Product: {product.name} (Created: {created})")
    
    # 4. Create an order
    tracking_num = f"TEST-{uuid.uuid4().hex[:8].upper()}"
    order = Order.objects.create(
        user=user,
        first_name='Test',
        last_name='User',
        email='krishnananbu99@gmail.com', # Use user's email for testing delivery if allowed
        phone='1234567890',
        address='123 Test St',
        city='Test City',
        state='Test State',
        zip_code='12345',
        subtotal=product.price,
        total_amount=product.price + Decimal('10.00'),
        status='pending',
        tracking_number=tracking_num
    )
    print(f"Order created: #{order.id} with tracking: {order.tracking_number}")
    
    # 5. Create order item
    OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=1
    )
    print("Order item created.")
    
    # 6. Update status to trigger signal
    print("Updating order status to 'processing'...")
    order.status = 'processing'
    order.save()
    
    # 7. Create OrderStatus record (this also triggers create_order_status_history signal)
    print("Creating OrderStatus update...")
    OrderStatus.objects.create(
        order=order,
        status='shipped',
        note='Package has been shipped'
    )
    
    # Refresh order from DB
    order.refresh_from_db()
    print(f"Final Order Status: {order.status}")
    print(f"Shipped Date: {order.shipped_date}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    run_test()
