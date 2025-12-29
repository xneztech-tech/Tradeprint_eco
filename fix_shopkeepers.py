"""
Script to create PrintShop records for existing shopkeeper users
Run this with: python manage.py shell < fix_shopkeepers.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradeprint_project.settings')
django.setup()

from tradeprint_backend.models import User, PrintShop

# Find all shopkeeper users without a PrintShop profile
shopkeeper_users = User.objects.filter(role='shopkeeper')

print(f"Found {shopkeeper_users.count()} shopkeeper users")

for user in shopkeeper_users:
    # Check if they already have a print shop
    if hasattr(user, 'print_shop_profile'):
        print(f"✓ {user.email} already has a PrintShop profile: {user.print_shop_profile.shop_name}")
    else:
        # Create a PrintShop for this user
        shop_name = f"{user.first_name}'s Print Shop" if user.first_name else f"{user.email}'s Print Shop"
        
        print_shop = PrintShop.objects.create(
            user=user,
            shop_name=shop_name,
            contact_phone="0000000000",  # Default phone - should be updated
            contact_email=user.email,
            location="Unknown",  # Default location - should be updated
            address="",
            postcode="",
            business_registration_number="",
            tax_id="",
            daily_capacity=50,
            monthly_capacity=1000,
            status='active'
        )
        
        print(f"✓ Created PrintShop '{shop_name}' for {user.email}")

print("\nDone! All shopkeeper users now have PrintShop profiles.")
print("Note: Please update the contact phone, location, and other details for these shops.")
