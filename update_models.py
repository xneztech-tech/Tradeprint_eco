import sys

# Read the file
with open(r'd:\fiverr\Tradeprint_eco\tradeprint_backend\models.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Customer model to insert
customer_model = '''

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

'''

# Insert at line 299 (before line 300 which is "class Order")
lines.insert(299, customer_model)

# Now update the Order model to add customer foreign key
# Find the line with "user = models.ForeignKey(User" in Order model
for i, line in enumerate(lines):
    if i > 299 and 'user = models.ForeignKey(User' in line and 'Order' in ''.join(lines[max(0,i-30):i]):
        # Insert customer foreign key after user field
        lines.insert(i+1, '    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name=\'orders\')\n')
        lines.insert(i+2, '    \n')
        lines.insert(i+3, '    # Shipping Address (can be different from customer\'s default address)\n')
        break

# Rename fields in Order model from first_name, last_name, etc. to shipping_first_name, etc.
for i, line in enumerate(lines):
    if i > 299:  # After Customer model
        if '    # Customer Details' in line:
            lines[i] = line.replace('# Customer Details', '# Shipping Address')
        elif '    first_name = models.CharField(max_length=100)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('first_name', 'shipping_first_name')
        elif '    last_name = models.CharField(max_length=100)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('last_name', 'shipping_last_name')
        elif '    email = models.EmailField()' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('email', 'shipping_email')
        elif '    phone = models.CharField(max_length=20)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('phone', 'shipping_phone')
        elif '    # Address' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = ''  # Remove this comment as we already have "# Shipping Address"
        elif '    address = models.CharField(max_length=255)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('address', 'shipping_address')
        elif '    city = models.CharField(max_length=100)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('city', 'shipping_city')
        elif '    postcode = models.CharField(max_length=20)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('postcode', 'shipping_postcode')
        elif '    country = models.CharField(max_length=100)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('country', 'shipping_country')
        elif '    state = models.CharField(max_length=100, blank=True)' in line and 'Order' in ''.join(lines[max(0,i-50):i]):
            lines[i] = line.replace('state', 'shipping_state')
        elif 'return f"Order {self.order_number} - {self.first_name} {self.last_name}"' in line:
            lines[i] = line.replace('self.first_name', 'self.shipping_first_name').replace('self.last_name', 'self.shipping_last_name')

# Write back
with open(r'd:\fiverr\Tradeprint_eco\tradeprint_backend\models.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Customer model added and Order model updated successfully!")
