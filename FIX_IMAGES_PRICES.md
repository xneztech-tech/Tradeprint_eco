# Fix for Images and Prices Not Displaying

## Issue 1: Images Not Showing

### Problem:
MEDIA_URL and MEDIA_ROOT are not configured in settings.py

### Solution:

Add these lines to `d:\fiverr\Tradeprint_eco\tradeprint_project\settings.py`:

```python
# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Then in `urls.py` (main project urls.py), add:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing patterns
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Issue 2: Prices Not Showing

### Problem:
The product might not have quantity_tiers data, or the JavaScript isn't finding the data

### Quick Fix - Add Default Sample Data:

In your product template, add this fallback right after the product config div starts (around line 395):

```html
<!-- Add default data if product doesn't have it -->
{% if not product.quantity_tiers %}
<script>
// Add sample data for testing
const sampleTiers = [
    {quantity: 50, saver_price: 12.50, standard_price: 15.00, express_price: 18.50},
    {quantity: 100, saver_price: 18.00, standard_price: 21.00, express_price: 25.00},
    {quantity: 250, saver_price: 32.50, standard_price: 38.00, express_price: 45.00},
    {quantity: 500, saver_price: 55.00, standard_price: 65.00, express_price: 78.00}
];
</script>
{% endif %}
```

## Issue 3: Price Not Updating

### Fix the JavaScript updatePrice() function:

Replace the updatePrice function (around line 600) with this improved version:

```javascript
function updatePrice() {
    const selectedQty = document.querySelector('.qty-btn.active');
    const selectedDelivery = document.querySelector('.delivery-card.active');
    
    if (selectedQty && selectedDelivery) {
        let price = 0;
        const deliveryText = selectedDelivery.querySelector('.delivery-name').textContent;
        
        // Determine which delivery type
        if (deliveryText.includes('Saver') || deliveryText.includes('💰')) {
            price = parseFloat(selectedQty.getAttribute('data-saver') || 0);
        } else if (deliveryText.includes('Express') || deliveryText.includes('⚡')) {
            price = parseFloat(selectedQty.getAttribute('data-express') || 0);
        } else {
            price = parseFloat(selectedQty.getAttribute('data-standard') || 0);
        }
        
        // Update the price display
        const priceElement = document.getElementById('currentPrice');
        if (priceElement && price > 0) {
            priceElement.textContent = '£' + price.toFixed(2);
        }
    }
}
```

## Quick Test - Add Sample Product Data

In Django Admin, add a product with this JSON data:

### Material Options:
```json
[
    {"name": "350gsm Silk", "price_modifier": 0},
    {"name": "300gsm Kraft", "price_modifier": 5},
    {"name": "400gsm Uncoated", "price_modifier": 3}
]
```

### Size Options:
```json
[
    {"name": "85mmx110mm", "price_modifier": 0},
    {"name": "90mmx50mm", "price_modifier": 2},
    {"name": "A7", "price_modifier": 1}
]
```

### Quantity Tiers:
```json
[
    {"quantity": 50, "saver_price": 12.50, "standard_price": 15.00, "express_price": 18.50},
    {"quantity": 100, "saver_price": 18.00, "standard_price": 21.00, "express_price": 25.00},
    {"quantity": 250, "saver_price": 32.50, "standard_price": 38.00, "express_price": 45.00},
    {"quantity": 500, "saver_price": 55.00, "standard_price": 65.00, "express_price": 78.00},
    {"quantity": 1000, "saver_price": 95.00, "standard_price": 110.00, "express_price": 130.00}
]
```

### Delivery Options:
```json
[
    {"name": "Saver", "days": "5-7", "price": 0},
    {"name": "Standard", "days": "3-4", "price": 5},
    {"name": "Express", "days": "1-2", "price": 15}
]
```

## Checklist:

- [ ] Add MEDIA_URL and MEDIA_ROOT to settings.py
- [ ] Add media URL patterns to urls.py
- [ ] Create 'media' folder in project root
- [ ] Add product with JSON data in Django Admin
- [ ] Upload at least one product image
- [ ] Test the product page
- [ ] Check if price updates when clicking quantity/delivery

## Debug Tips:

1. **Check if product exists**: Open browser console and type `console.log({{ product.id }})`
2. **Check if data is there**: View page source and search for "data-saver"
3. **Check JavaScript errors**: Open browser DevTools (F12) → Console tab
4. **Check image paths**: Right-click on broken image → "Open in new tab" to see the URL

If images still don't show, they might be using placeholder paths. Make sure to upload actual images in Django Admin!
