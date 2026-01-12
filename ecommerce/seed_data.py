import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import Category, Product, Brand
from django.utils.text import slugify

def create_sample_data():
    print("Creating sample data...")
    
    # Create Categories
    categories = ['Electronics', 'Fashion', 'Home & Living', 'Sports']
    cat_objs = {}
    for cat_name in categories:
        cat, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name), 'description': f'Premium {cat_name} collection'}
        )
        cat_objs[cat_name] = cat
        if created:
            print(f"Created category: {cat_name}")

    # Create Brands
    brands = ['Apple', 'Samsung', 'Nike', 'Adidas', 'Sony']
    brand_objs = {}
    for brand_name in brands:
        brand, created = Brand.objects.get_or_create(
            name=brand_name,
            defaults={'slug': slugify(brand_name)}
        )
        brand_objs[brand_name] = brand
        if created:
            print(f"Created brand: {brand_name}")

    # Create Products
    products = [
        {
            'name': 'iPhone 15 Pro',
            'category': cat_objs['Electronics'],
            'brand': brand_objs['Apple'],
            'price': 999.00,
            'description': 'The ultimate iPhone experience.',
            'stock': 10,
            'featured': True
        },
        {
            'name': 'Nike Air Max',
            'category': cat_objs['Fashion'],
            'brand': brand_objs['Nike'],
            'price': 120.00,
            'description': 'Comfortable and stylish sneakers.',
            'stock': 25,
            'featured': True
        },
        {
            'name': 'Sony WH-1000XM5',
            'category': cat_objs['Electronics'],
            'brand': brand_objs['Sony'],
            'price': 349.00,
            'description': 'Industry-leading noise canceling headphones.',
            'stock': 15,
            'featured': False
        },
        {
            'name': 'Adidas Ultraboost',
            'category': cat_objs['Sports'],
            'brand': brand_objs['Adidas'],
            'price': 180.00,
            'description': 'High-performance running shoes.',
            'stock': 0,
            'featured': False
        }
    ]

    for p_data in products:
        p, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'slug': slugify(p_data['name']),
                'category': p_data['category'],
                'brand': p_data['brand'],
                'price': p_data['price'],
                'description': p_data['description'],
                'stock': p_data['stock'],
                'available': True,
                'featured': p_data['featured']
            }
        )
        if created:
            print(f"Created product: {p_data['name']}")

if __name__ == "__main__":
    create_sample_data()
