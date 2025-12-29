from django.core.management.base import BaseCommand
from tradeprint_backend.models import User, PrintShop


class Command(BaseCommand):
    help = 'Create PrintShop records for existing shopkeeper users who don\'t have them'

    def handle(self, *args, **options):
        # Find all shopkeeper users
        shopkeeper_users = User.objects.filter(role='shopkeeper')
        
        self.stdout.write(f"Found {shopkeeper_users.count()} shopkeeper users\n")
        
        created_count = 0
        existing_count = 0
        
        for user in shopkeeper_users:
            # Check if they already have a print shop
            if hasattr(user, 'print_shop_profile'):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ {user.email} already has a PrintShop profile: {user.print_shop_profile.shop_name}"
                    )
                )
                existing_count += 1
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
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Created PrintShop '{shop_name}' for {user.email}"
                    )
                )
                created_count += 1
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"\nDone!"))
        self.stdout.write(f"  - Existing PrintShops: {existing_count}")
        self.stdout.write(f"  - Created PrintShops: {created_count}")
        self.stdout.write("\nNote: Please update the contact phone, location, and other details for new shops.\n")
