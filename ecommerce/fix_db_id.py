
from django.db import connection

def fix_id_column():
    with connection.cursor() as cursor:
        try:
            print("Trying to fix id column for shop_order...")
            # Check if sequence exists
            cursor.execute("SELECT exists (SELECT 1 FROM pg_class WHERE relkind = 'S' AND relname = 'shop_order_id_seq')")
            seq_exists = cursor.fetchone()[0]
            
            if not seq_exists:
                print("Sequence shop_order_id_seq does not exist. Creating it...")
                cursor.execute("CREATE SEQUENCE shop_order_id_seq")
            
            # Set default for id
            print("Setting default for id column...")
            cursor.execute("ALTER TABLE shop_order ALTER COLUMN id SET DEFAULT nextval('shop_order_id_seq')")
            
            # Ensure id is primary key if not already
            try:
                cursor.execute("ALTER TABLE shop_order ADD PRIMARY KEY (id)")
                print("Added primary key to id.")
            except Exception as e:
                print(f"Primary key might already exist: {e}")
                
            print("Successfully fixed id column.")
        except Exception as e:
            print(f"Error fixing id column: {e}")

if __name__ == "__main__":
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
    django.setup()
    fix_id_column()
