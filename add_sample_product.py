import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradeprint_project.settings')
django.setup()

from tradeprint_backend.models import Product, Category

# Create or get a category first
category, created = Category.objects.get_or_create(
    name="Print Products",
    defaults={
        'slug': 'print-products',
        'short_description': 'Professional printing products',
        'status': 'active'
    }
)

# Create the Business Cards product
product = Product.objects.create(
    name="Business Cards",
    slug="business-cards",
    category=category,
    short_description="Professional business cards printed on premium quality card stock",
    full_description="High-quality business cards perfect for networking and professional use. Available in various finishes and sizes. Our business cards are printed on premium card stock with a choice of finishes including matt, gloss, and uncoated options.",
    tags="business, cards, professional, networking",
    base_price=25.00,
    sides_printed="single",
    double_sided_price=5.00,
    allow_different_designs=False,
    max_different_designs=1,
    stock_quantity=1000,
    min_order_quantity=250,
    status="active",
    
    # JSON fields
    material_options=[
        {"name": "400gsm Silk", "price_modifier": 0.00},
        {"name": "400gsm Matt", "price_modifier": 0.00},
        {"name": "450gsm Uncoated", "price_modifier": 2.00}
    ],
    size_options=[
        {"name": "85x55mm (Standard)", "price_modifier": 0.00},
        {"name": "90x50mm", "price_modifier": 2.00}
    ],
    lamination_options=[
        {"name": "None", "price_modifier": 0.00},
        {"name": "Matt Lamination", "price_modifier": 5.00},
        {"name": "Gloss Lamination", "price_modifier": 5.00}
    ],
    banding_options=[
        {"name": "No Banding", "price_modifier": 0.00},
        {"name": "Banded in 50s", "price_modifier": 3.00},
        {"name": "Banded in 100s", "price_modifier": 5.00}
    ],
    quantity_tiers=[
        {"quantity": 250, "price": 25.00},
        {"quantity": 500, "price": 40.00},
        {"quantity": 1000, "price": 65.00},
        {"quantity": 2500, "price": 140.00},
        {"quantity": 5000, "price": 250.00}
    ],
    delivery_options=[
        {"name": "Saver Delivery", "days": "5-7 working days", "price": 0.00},
        {"name": "Standard Delivery", "days": "3-5 working days", "price": 10.00},
        {"name": "Express Delivery", "days": "1-2 working days", "price": 25.00}
    ]
)

print(f"✅ Product created successfully!")
print(f"Product ID: {product.id}")
print(f"Product Name: {product.name}")
print(f"Base Price: £{product.base_price}")
print(f"Stock: {product.stock_quantity}")
print(f"Status: {product.status}")
print(f"\nYou can now view it at: http://127.0.0.1:8000/product-list/")
