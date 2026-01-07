
from django.db import connection

def patch_db():
    queries = [
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS state VARCHAR(100)",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS zip_code VARCHAR(10)",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS tracking_number VARCHAR(100)",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS estimated_delivery DATE",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS shipping_method VARCHAR(50)",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS order_notes TEXT",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS admin_notes TEXT",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS shipped_date TIMESTAMP WITH TIME ZONE",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS delivered_date TIMESTAMP WITH TIME ZONE",
        "ALTER TABLE shop_order ADD COLUMN IF NOT EXISTS payment_date TIMESTAMP WITH TIME ZONE",
    ]
    
    with connection.cursor() as cursor:
        for query in queries:
            try:
                print(f"Executing: {query}")
                cursor.execute(query)
            except Exception as e:
                print(f"Error executing {query}: {e}")

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    django.setup()
    patch_db()
