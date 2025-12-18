# Quick Start Guide: Making Cart & Checkout Work

## ✅ Backend is Complete!

The backend is **100% functional**. Here's what's working:
- ✅ Database models (Cart, CartItem)
- ✅ All cart views (add, view, update, remove)
- ✅ API endpoints
- ✅ Product page integration
- ✅ AJAX add to cart functionality

## 🎯 What You Need to Do

### Step 1: Test Add to Cart (Already Works!)

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Go to a product page:**
   ```
   http://127.0.0.1:8000/product-detail/1/
   ```

3. **Configure and add to cart:**
   - Select material, size, quantity, delivery
   - Click "Add to Cart"
   - You should see a success message!
   - Cart count in header should update automatically

### Step 2: Update Cart Page Template

**File to edit:** `tradeprint_app/templates/frontend/cart.html`

**Find lines 710-790** (the static product rows) and **replace with:**

```django
{% load static %}
{% if cart_items %}
    {% for item in cart_items %}
    <tr>
        <td data-label="Product" class="ec-cart-pro-name">
            <a href="{% url 'product_detail' item.product.id %}">
                {% if item.product.main_image %}
                <img class="ec-cart-pro-img mr-4" 
                     src="{{ item.product.main_image.url }}" 
                     alt="{{ item.product.name }}" />
                {% endif %}
                {{ item.product.name }}
            </a>
            <br>
            <small style="color: #666;">{{ item.configuration_summary }}</small>
        </td>
        <td data-label="Price" class="ec-cart-pro-price">
            <span class="amount">£{{ item.unit_price }}</span>
        </td>
        <td data-label="Quantity" class="ec-cart-pro-qty" style="text-align: center;">
            <div class="cart-qty-plus-minus">
                <input class="cart-plus-minus" type="text" 
                       name="cartqtybutton" value="{{ item.quantity }}" 
                       data-item-id="{{ item.id }}" />
            </div>
        </td>
        <td data-label="Total" class="ec-cart-pro-subtotal">
            £{{ item.total_price|floatformat:2 }}
        </td>
        <td data-label="Remove" class="ec-cart-pro-remove">
            <a href="{% url 'remove_from_cart' item.id %}" 
               onclick="return confirm('Remove this item?')">
                <i class="ecicon eci-trash-o"></i>
            </a>
        </td>
    </tr>
    {% endfor %}
{% else %}
    <tr>
        <td colspan="5" style="text-align: center; padding: 40px;">
            <h4>Your cart is empty</h4>
            <p>Start shopping to add items to your cart!</p>
            <a href="{% url 'home' %}" class="btn btn-primary">Continue Shopping</a>
        </td>
    </tr>
{% endif %}
```

**Also update the checkout button (around line 798):**

```django
<div class="ec-cart-update-bottom">
    {% if cart_items %}
    <a href="{% url 'checkout' %}" class="btn btn-primary">
        Proceed to Checkout
    </a>
    {% endif %}
</div>
```

**Update the cart summary sidebar (find the summary section, around line 870-900):**

```django
<div class="ec-sidebar-block">
    <div class="ec-sb-title">
        <h3 class="ec-sidebar-title">Cart Summary</h3>
    </div>
    <div class="ec-sb-block-content">
        <div class="ec-cart-summary-bottom">
            <div class="ec-cart-summary">
                <div>
                    <span class="text-left">Sub-Total</span>
                    <span class="text-right">£{{ subtotal|floatformat:2 }}</span>
                </div>
                <div>
                    <span class="text-left">VAT (20%)</span>
                    <span class="text-right">£{{ vat|floatformat:2 }}</span>
                </div>
                <div class="ec-cart-summary-total">
                    <span class="text-left">Total Amount</span>
                    <span class="text-right">£{{ total|floatformat:2 }}</span>
                </div>
            </div>
            {% if cart_items %}
            <div class="ec-cart-summary-button">
                <a href="{% url 'checkout' %}" class="btn btn-primary w-100">
                    Proceed to Checkout
                </a>
            </div>
            {% endif %}
        </div>
    </div>
</div>
```

### Step 3: Add JavaScript for Quantity Updates

**Add this script before the closing `</body>` tag in cart.html:**

```html
<script>
// Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update cart quantity
document.querySelectorAll('.cart-plus-minus').forEach(input => {
    input.addEventListener('change', function() {
        const itemId = this.dataset.itemId;
        const quantity = parseInt(this.value);
        
        if (quantity < 1) {
            if (confirm('Remove this item from cart?')) {
                window.location.href = `/cart/remove/${itemId}/`;
            } else {
                this.value = 1;
            }
            return;
        }
        
        const formData = new FormData();
        formData.append('quantity', quantity);
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        
        fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Reload page to show updated totals
                location.reload();
            } else {
                alert('Error updating cart: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the cart');
        });
    });
});
</script>
```

### Step 4: Update Side Cart (Optional but Recommended)

**Find the side cart section in your base template or header** (look for `id="ec-side-cart"`).

**Replace the static cart items with:**

```django
<ul class="eccart-pro-items">
    {% for item in cart_items|slice:":3" %}
    <li>
        <a href="{% url 'product_detail' item.product.id %}" class="sidecart_pro_img">
            {% if item.product.main_image %}
            <img src="{{ item.product.main_image.url }}" alt="{{ item.product.name }}">
            {% endif %}
        </a>
        <div class="ec-pro-content">
            <a href="{% url 'product_detail' item.product.id %}" class="cart_pro_title">
                {{ item.product.name }}
            </a>
            <span class="cart-price">
                <span>£{{ item.unit_price }}</span> x {{ item.quantity }}
            </span>
            <a href="{% url 'remove_from_cart' item.id %}" class="remove" 
               onclick="return confirm('Remove this item?')">×</a>
        </div>
    </li>
    {% empty %}
    <li style="text-align: center; padding: 20px;">
        <p>Your cart is empty</p>
    </li>
    {% endfor %}
</ul>
```

**Update the side cart totals:**

```django
<div class="cart-sub-total">
    <table class="table cart-table">
        <tbody>
            <tr>
                <td class="text-left">Sub-Total :</td>
                <td class="text-right">£{{ subtotal|floatformat:2 }}</td>
            </tr>
            <tr>
                <td class="text-left">VAT (20%) :</td>
                <td class="text-right">£{{ vat|floatformat:2 }}</td>
            </tr>
            <tr>
                <td class="text-left">Total :</td>
                <td class="text-right primary-color">£{{ total|floatformat:2 }}</td>
            </tr>
        </tbody>
    </table>
</div>
<div class="cart_btn">
    <a href="{% url 'view_cart' %}" class="btn btn-primary">View Cart</a>
    <a href="{% url 'checkout' %}" class="btn btn-secondary">Checkout</a>
</div>
```

### Step 5: Update Checkout Page

**File:** `tradeprint_app/templates/frontend/checkout.html`

**Find the order summary section and add:**

```django
<div class="ec-checkout-summary">
    <h3 class="ec-checkout-title">Order Summary</h3>
    <div class="ec-checkout-summary-total">
        {% for item in cart_items %}
        <div class="checkout-summary-item">
            <div class="item-details">
                <span class="item-name">{{ item.product.name }}</span>
                <small class="item-config">{{ item.configuration_summary }}</small>
            </div>
            <div class="item-pricing">
                <span>{{ item.quantity }} x £{{ item.unit_price }}</span>
                <strong>£{{ item.total_price|floatformat:2 }}</strong>
            </div>
        </div>
        {% endfor %}
        
        <div class="checkout-summary-totals">
            <div class="summary-row">
                <span>Subtotal:</span>
                <span>£{{ subtotal|floatformat:2 }}</span>
            </div>
            <div class="summary-row">
                <span>VAT (20%):</span>
                <span>£{{ vat|floatformat:2 }}</span>
            </div>
            <div class="summary-row total">
                <strong>Total:</strong>
                <strong>£{{ total|floatformat:2 }}</strong>
            </div>
        </div>
    </div>
</div>
```

## 🎨 Optional: Add Context Processor for Global Cart Access

This makes cart data available in ALL templates automatically.

**1. Create file:** `tradeprint_backend/context_processors.py`

```python
def cart_context(request):
    """Make cart available in all templates"""
    from .views import get_or_create_cart
    
    cart = get_or_create_cart(request)
    return {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all()[:10],  # Limit for performance
        'cart_count': cart.total_items,
        'cart_subtotal': cart.subtotal,
        'cart_vat': cart.vat,
        'cart_total': cart.total
    }
```

**2. Update `settings.py`:**

Find the `TEMPLATES` setting and add the context processor:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tradeprint_backend.context_processors.cart_context',  # ADD THIS LINE
            ],
        },
    },
]
```

**Benefits:**
- Cart count automatically updates in header on every page
- Side cart always shows current items
- No need to pass cart data in every view

## 🧪 Testing Steps

1. **Add items to cart:**
   - Go to product page
   - Configure product
   - Click "Add to Cart"
   - Check header cart count updates

2. **View cart:**
   - Click cart icon or go to `/cart/`
   - See all items with configurations
   - Try updating quantities
   - Try removing items

3. **Checkout:**
   - Go to `/checkout/`
   - See order summary with all items
   - Verify totals are correct

4. **Side cart:**
   - Click cart icon in header
   - See mini cart with items
   - Click "View Cart" or "Checkout"

## 🐛 Troubleshooting

**Cart count not updating?**
- Make sure you added the context processor
- Check browser console for JavaScript errors
- Verify CSRF token is present

**Items not showing?**
- Check if cart_items is being passed to template
- Verify the view is using the correct template
- Check for template syntax errors

**Can't add to cart?**
- Check browser console for errors
- Verify CSRF token is present
- Check Django logs for backend errors

## 📝 Summary

**What's Done:**
- ✅ Complete backend (models, views, URLs)
- ✅ Database migrations
- ✅ Add to cart functionality
- ✅ Cart count updates
- ✅ Product page integration

**What You Need to Do:**
- 📝 Update cart.html template (copy-paste code above)
- 📝 Add JavaScript for quantity updates
- 📝 Update side cart in base template
- 📝 Update checkout.html template
- 📝 (Optional) Add context processor

**Time Estimate:** 15-30 minutes to update templates

The backend is rock-solid and ready to go. Just update the templates and you're done! 🚀
