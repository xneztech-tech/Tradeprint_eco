from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

class User(AbstractUser):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('shopkeeper', 'Shopkeeper'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]   # required when using createsuperuser

    def __str__(self):
        return self.email


# Main category

class Category(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    TRENDING_CHOICES = (
        ("top", "Top"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    trending = models.CharField(max_length=10, choices=TRENDING_CHOICES, default="medium")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    TRENDING_CHOICES = (
        ("top", "Top"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    category = models.ForeignKey(Category, related_name="subcategories", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    tags = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    trending = models.CharField(max_length=10, choices=TRENDING_CHOICES, default="medium")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.category.name} → {self.name}"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SubSubCategory(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    TRENDING_CHOICES = (
        ("top", "Top"),
        ("medium", "Medium"),
        ("low", "Low"),
    )

    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    trending = models.CharField(max_length=10, choices=TRENDING_CHOICES)

    def __str__(self):
        return f"{self.parent_category.name} → {self.sub_category.name} → {self.name}"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    
    # Category Relations
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    sub_sub_category = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Descriptions
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma separated tags")
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base price for the product",null=True, blank=True)
    
    # Material Options (JSON field to store multiple material options)
    # Example: [{"name": "130gsm Gloss Finish", "price_modifier": 0}, {"name": "170gsm Matt Finish", "price_modifier": 5}]
    material_options = models.JSONField(default=list, blank=True, help_text="Material options with price modifiers")
    
    # Size Options (JSON field)
    # Example: [{"name": "A5", "price_modifier": 0}, {"name": "A4", "price_modifier": 10}]
    size_options = models.JSONField(default=list, blank=True, help_text="Size options with price modifiers")
    
    # Printing Options
    SIDES_CHOICES = (
        ("single", "Single Sided"),
        ("double", "Double Sided"),
        ("both", "Both Available"),
    )
    sides_printed = models.CharField(max_length=20, choices=SIDES_CHOICES, default="both")
    double_sided_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Additional price for double sided")
    
    # Lamination Options (JSON field)
    # Example: [{"name": "None", "price_modifier": 0}, {"name": "Matt", "price_modifier": 15}, {"name": "Gloss", "price_modifier": 15}]
    lamination_options = models.JSONField(default=list, blank=True, help_text="Lamination options with price modifiers")
    
    # Banding Options (JSON field)
    # Example: [{"name": "None", "price_modifier": 0}, {"name": "50s", "price_modifier": 5}]
    banding_options = models.JSONField(default=list, blank=True, help_text="Banding options with price modifiers")
    
    # Different Designs Support
    allow_different_designs = models.BooleanField(default=False)
    max_different_designs = models.IntegerField(default=1, help_text="Maximum number of different designs allowed")
    
    # Quantity Tiers (JSON field for pricing grid)
    # Example: [{"quantity": 100, "price": 50}, {"quantity": 500, "price": 200}]
    quantity_tiers = models.JSONField(default=list, blank=True, help_text="Quantity-based pricing tiers")
    
    # Delivery Options (JSON field)
    # Example: [{"name": "Saver", "days": "5-7", "price": 0}, {"name": "Standard", "days": "3-5", "price": 10}]
    delivery_options = models.JSONField(default=list, blank=True, help_text="Delivery speed options with prices")
    
    # Images
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True)
    image_1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Stock & Status
    stock_quantity = models.IntegerField(default=0, help_text="Available stock quantity")
    min_order_quantity = models.IntegerField(default=1, help_text="Minimum order quantity")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Cart(models.Model):
    """Shopping cart for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Anonymous Cart {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        from decimal import Decimal
        total = sum(item.total_price for item in self.items.all())
        return Decimal(str(total)) if total else Decimal('0.00')

    @property
    def vat(self):
        from decimal import Decimal
        return self.subtotal * Decimal('0.20')  # 20% VAT

    @property
    def total(self):
        return self.subtotal + self.vat


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Product Configuration
    material = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    sides_printed = models.CharField(max_length=50, blank=True)
    lamination = models.CharField(max_length=255, blank=True)
    banding = models.CharField(max_length=255, blank=True)
    
    # Artwork - Temporary storage until order
    artwork_file = models.FileField(upload_to='artwork/cart/', blank=True, null=True)
    
    # Quantity and Delivery
    quantity = models.IntegerField(default=1)
    delivery_service = models.CharField(max_length=50, blank=True)  # Saver, Standard, Express
    delivery_days = models.CharField(max_length=50, blank=True)
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return (self.unit_price * self.quantity) + self.delivery_price

    @property
    def configuration_summary(self):
        """Returns a readable summary of the product configuration"""
        config = []
        if self.material:
            config.append(f"Material: {self.material}")
        if self.size:
            config.append(f"Size: {self.size}")
        if self.sides_printed:
            config.append(f"Sides: {self.sides_printed}")
        if self.lamination:
            config.append(f"Lamination: {self.lamination}")
        if self.banding:
            config.append(f"Banding: {self.banding}")
        if self.delivery_service:
            config.append(f"Delivery: {self.delivery_service} ({self.delivery_days})")
        return " | ".join(config)




class Customer(models.Model):
    """Customer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer_profile')
    
    # Personal Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Default Address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
    )
    
    # Order Information
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Shipping Address (can be different from customer's default address)
    shipping_first_name = models.CharField(max_length=100)
    shipping_last_name = models.CharField(max_length=100)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=20)
    
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True)
    
    # Delivery
    delivery_method = models.CharField(max_length=50, default='standard')
    delivery_notes = models.TextField(blank=True)
    
    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Functionality
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    is_sent_to_printer = models.BooleanField(default=False)
    shipping_label_url = models.CharField(max_length=500, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    
    # Platform Admin Fields
    is_artwork_verified = models.BooleanField(default=False)
    invoice_pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    # Auto-Assignment
    assigned_shop = models.ForeignKey('PrintShop', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.shipping_first_name} {self.shipping_last_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            from datetime import datetime
            # Generate order number: ORD-YYYYMMDD-XXXX
            date_str = datetime.now().strftime('%Y%m%d')
            random_str = ''.join(random.choices(string.digits, k=4))
            self.order_number = f"ORD-{date_str}-{random_str}"
            
        # Auto-assign logic (Smart Assignment)
        if not self.assigned_shop:
            # Fetch valid candidates
            candidate_shops = PrintShop.objects.filter(status='active', user__role='shopkeeper')
            
            best_shop = None
            best_score = -1
            
            # Normalize order data
            target_city = (self.shipping_city or "").lower().strip()
            is_urgent = self.delivery_method in ['express', 'next_day']
            
            for shop in candidate_shops:
                score = 0
                shop_location = shop.location.lower().strip()
                
                # 1. Location Matching (10 pts)
                # Exact city match is ideal for speed and shipping costs
                if shop_location and target_city and shop_location == target_city:
                    score += 10
                elif shop_location and target_city and shop_location in target_city:
                    score += 5  # Partial match
                    
                # 2. Delivery Speed / Urgency (5 pts)
                # If order is urgent, a local shop is critical
                if is_urgent:
                    if score >= 5: # If it's at least a partial local match
                        score += 5
                
                # Check current load (Tie-breaker)
                # active_load = shop.assigned_orders.filter(status__in=['pending', 'processing']).count()
                # score -= (active_load * 0.1) # Penalize busy shops slightly
                
                if score > best_score:
                    best_score = score
                    best_shop = shop
            
            # Fallback: If no matches (score 0), pick the first active one or keep best found
            if best_shop:
                self.assigned_shop = best_shop
            elif candidate_shops.exists():
                # If no location match found, just assign to the first available to ensure it gets processed
                self.assigned_shop = candidate_shops.first()
            
        super().save(*args, **kwargs)

        # Generate barcode if it doesn't exist (need PK to be saved first if we were using it, but we use order_number)
        if not self.barcode_image and self.order_number:
            import barcode
            from barcode.writer import ImageWriter
            from io import BytesIO
            from django.core.files import File

            # Generate barcode
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(self.order_number, writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            
            # Save to field
            self.barcode_image.save(f'{self.order_number}.png', File(buffer), save=False)
            super().save(update_fields=['barcode_image'])


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    # Product Configuration
    material = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    sides_printed = models.CharField(max_length=50, blank=True)
    lamination = models.CharField(max_length=255, blank=True)
    banding = models.CharField(max_length=255, blank=True)
    
    # Artwork
    artwork_file = models.FileField(upload_to='artwork/orders/', blank=True, null=True)
    
    # Quantity and Delivery
    quantity = models.IntegerField(default=1)
    delivery_service = models.CharField(max_length=50, blank=True)
    delivery_days = models.CharField(max_length=50, blank=True)
    
    # Pricing (snapshot at time of order)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Deleted Product'}"


class PrintShop(models.Model):
    """Printing Shop / Partner"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='print_shop_profile')
    shop_name = models.CharField(max_length=150)
    
    # Contact Information
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Address Information
    location = models.CharField(max_length=255)  # City/Region for simple matching
    address = models.TextField(blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    
    # Business Information
    business_registration_number = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Capacity & Operations
    daily_capacity = models.IntegerField(default=50, help_text="Maximum orders per day")
    monthly_capacity = models.IntegerField(default=1000, help_text="Maximum orders per month")
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.shop_name
    
    class Meta:
        verbose_name = "Print Shop"
        verbose_name_plural = "Print Shops"
        ordering = ['-created_at']
