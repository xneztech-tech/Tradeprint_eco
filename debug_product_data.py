# Debug script to check product data
# Run this in Django shell: python manage.py shell

from tradeprint_backend.models import Product
import json

# Get product 4
product = Product.objects.get(id=4)

print("=== PRODUCT 4 DEBUG INFO ===\n")
print(f"Product Name: {product.name}")
print(f"Base Price: {product.base_price}")
print("\n--- Quantity Tiers ---")
print(f"Raw data: {product.quantity_tiers}")
print(f"Type: {type(product.quantity_tiers)}")

if product.quantity_tiers:
    print("\nParsed tiers:")
    for i, tier in enumerate(product.quantity_tiers):
        print(f"\nTier {i+1}:")
        print(f"  Type: {type(tier)}")
        print(f"  Keys: {tier.keys() if isinstance(tier, dict) else 'Not a dict'}")
        print(f"  Data: {tier}")
        
        if isinstance(tier, dict):
            print(f"  quantity: {tier.get('quantity', 'MISSING')}")
            print(f"  saver_price: {tier.get('saver_price', 'MISSING')}")
            print(f"  standard_price: {tier.get('standard_price', 'MISSING')}")
            print(f"  express_price: {tier.get('express_price', 'MISSING')}")

print("\n--- Material Options ---")
print(f"Raw data: {product.material_options}")

print("\n--- Size Options ---")
print(f"Raw data: {product.size_options}")

print("\n--- Delivery Options ---")
print(f"Raw data: {product.delivery_options}")
