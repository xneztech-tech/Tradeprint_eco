-- Sample Product Data for Testing
-- Run this in Django shell or add via Admin

-- Example: Adding a test product via Django shell
-- python manage.py shell

from tradeprint_backend.models import Product, Category

# Create a category first (if not exists)
category, created = Category.objects.get_or_create(
    name="Business Cards",
    defaults={'slug': 'business-cards'}
)

# Create a sample product
product = Product.objects.create(
    name="Folded Business Cards",
    slug="folded-business-cards",
    category=category,
    short_description="High-quality folded business cards with twice the space of standard cards.",
    full_description="<p>Folded Business Card printing gives you twice as much space as a standard card. Ideal for showcasing price-lists, mini menus or appointment tables.</p>",
    base_price=55.00,
    status="active",
    
    # Material Options
    material_options=[
        {"name": "350gsm Silk", "price_modifier": 0},
        {"name": "300gsm Kraft", "price_modifier": 5},
        {"name": "400gsm Uncoated", "price_modifier": 3}
    ],
    
    # Size Options
    size_options=[
        {"name": "85mmx110mm", "price_modifier": 0},
        {"name": "90mmx50mm", "price_modifier": 2},
        {"name": "A7", "price_modifier": 1}
    ],
    
    # Quantity Tiers with Pricing
    quantity_tiers=[
        {
            "quantity": 50,
            "saver_price": 12.50,
            "standard_price": 15.00,
            "express_price": 18.50
        },
        {
            "quantity": 100,
            "saver_price": 18.00,
            "standard_price": 21.00,
            "express_price": 25.00
        },
        {
            "quantity": 250,
            "saver_price": 32.50,
            "standard_price": 38.00,
            "express_price": 45.00
        },
        {
            "quantity": 500,
            "saver_price": 55.00,
            "standard_price": 65.00,
            "express_price": 78.00
        },
        {
            "quantity": 1000,
            "saver_price": 95.00,
            "standard_price": 110.00,
            "express_price": 130.00
        },
        {
            "quantity": 2500,
            "saver_price": 210.00,
            "standard_price": 245.00,
            "express_price": 290.00
        }
    ],
    
    # Delivery Options
    delivery_options=[
        {"name": "Saver", "days": "5-7", "price": 0},
        {"name": "Standard", "days": "3-4", "price": 5},
        {"name": "Express", "days": "1-2", "price": 15}
    ],
    
    # Other options
    sides_printed="both",
    min_order_quantity=50,
    stock_quantity=10000
)

print(f"Product created with ID: {product.id}")
print(f"Visit: http://127.0.0.1:8000/product/{product.id}/")
