# 🔧 Cart Error Troubleshooting Guide

## ✅ Fixes Applied

I've just fixed the "An error occurred while adding to cart" issue. Here's what was done:

### 1. **Added CSRF Token** ✅
- Added `{% csrf_token %}` to the product page template
- This is required for Django security

### 2. **Improved CSRF Token Retrieval** ✅
- Added `getCookie()` function to get CSRF token from cookies
- Falls back to form field if cookie not available
- Shows clear error if token is missing

### 3. **Better Error Handling** ✅
- Now shows the actual error message from the server
- Helps identify what went wrong
- Logs errors to browser console

## 🧪 How to Test

1. **Refresh the page** (Ctrl + F5 to clear cache)
2. **Open browser console** (F12)
3. **Try adding to cart again**
4. **Check for error messages**

## 🔍 If Still Not Working

### Step 1: Check Browser Console

Press **F12** and look for errors. Common issues:

**Error: "Security token missing"**
- Solution: Refresh the page
- The CSRF token should now load

**Error: "403 Forbidden"**
- Solution: Check Django settings
- Ensure CSRF middleware is enabled

**Error: "500 Internal Server Error"**
- Solution: Check Django server logs
- Look for Python errors

### Step 2: Check Django Server Logs

Look at the terminal where you ran `python manage.py runserver`

Common errors:

**"Product matching query does not exist"**
```
Solution: The product ID is invalid
Check: {{ product.id }} in the template
```

**"IntegrityError"**
```
Solution: Database constraint violation
Check: All required fields are being sent
```

**"AttributeError"**
```
Solution: Missing field in model or view
Check: Models have all required fields
```

### Step 3: Test with Browser Network Tab

1. Open **Developer Tools** (F12)
2. Go to **Network** tab
3. Click **Add to Cart**
4. Look for the POST request to `/cart/add/`
5. Check:
   - Request payload (should have all product data)
   - Response status (should be 200)
   - Response body (should show success or error)

### Step 4: Verify Data Being Sent

The following data should be sent to the backend:

```javascript
{
    product_id: "1",
    quantity: "100",
    material: "130gsm Gloss",
    size: "A5",
    sides_printed: "Single Sided",
    lamination: "None",
    delivery_service: "Standard",
    delivery_days: "3-5 working days",
    unit_price: "27.64",
    delivery_price: "0",
    csrfmiddlewaretoken: "..."
}
```

## 🐛 Common Issues & Solutions

### Issue 1: CSRF Token Missing
**Symptom:** "Security token missing" alert

**Solution:**
```html
<!-- Make sure this is in the template -->
{% csrf_token %}
```

### Issue 2: Product ID Not Found
**Symptom:** "Product matching query does not exist"

**Solution:**
```django
<!-- Check the product ID is valid -->
{{ product.id }}  <!-- Should show a number -->
```

### Issue 3: Quantity Not Selected
**Symptom:** "Please select a quantity" alert

**Solution:**
- Make sure quantity buttons have the `qty-btn` class
- Ensure one is marked as `active` by default

### Issue 4: Price Not Updating
**Symptom:** Price shows £0.00

**Solution:**
```javascript
// Check if quantity tiers exist
{% if product.quantity_tiers %}
    // Pricing should work
{% else %}
    // No pricing data!
{% endif %}
```

### Issue 5: CORS Error
**Symptom:** "Access-Control-Allow-Origin" error

**Solution:**
```python
# In settings.py, add:
CORS_ALLOW_ALL_ORIGINS = True  # For development only!
```

## 📊 Debugging Checklist

- [ ] CSRF token is present in the page
- [ ] Product ID is valid
- [ ] Quantity is selected
- [ ] Price is calculated correctly
- [ ] Browser console shows no errors
- [ ] Django server is running
- [ ] Database migrations are applied
- [ ] Cart models exist in database

## 🔬 Advanced Debugging

### Check if Cart Models Exist

```bash
python manage.py shell
```

```python
from tradeprint_backend.models import Cart, CartItem
print(Cart.objects.all())
print(CartItem.objects.all())
```

### Test Add to Cart Manually

```python
from tradeprint_backend.models import Cart, CartItem, Product
from decimal import Decimal

# Get or create a cart
cart = Cart.objects.create()

# Get a product
product = Product.objects.first()

# Create cart item
item = CartItem.objects.create(
    cart=cart,
    product=product,
    quantity=100,
    material="Test Material",
    size="A5",
    unit_price=Decimal("27.64"),
    delivery_price=Decimal("0")
)

print(f"Cart item created: {item}")
print(f"Cart total: {cart.total}")
```

### Check CSRF Cookie

In browser console:
```javascript
document.cookie.split(';').forEach(c => console.log(c.trim()));
```

Should see: `csrftoken=...`

## 🎯 Quick Fix Commands

### Restart Server
```bash
# Stop server (Ctrl+C)
python manage.py runserver
```

### Clear Browser Cache
```
Ctrl + Shift + Delete
Or
Ctrl + F5 (hard refresh)
```

### Reapply Migrations
```bash
python manage.py migrate
```

### Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

## 📝 What Should Happen

When everything works correctly:

1. **User clicks "Add to Cart"**
2. **JavaScript validates** (quantity selected)
3. **CSRF token retrieved** (from cookie or form)
4. **AJAX POST request** sent to `/cart/add/`
5. **Django view processes** the request
6. **Cart/CartItem created** in database
7. **JSON response** sent back
8. **Success alert** shown to user
9. **Cart count updates** in header

## 🆘 Still Not Working?

If you've tried everything above and it's still not working:

1. **Check the exact error message** in the alert
2. **Look at Django server logs** for Python errors
3. **Check browser console** for JavaScript errors
4. **Verify database** has Cart and CartItem tables
5. **Test with a simple product** (minimal configuration)

## 📞 Error Messages Explained

| Error Message | Meaning | Solution |
|---------------|---------|----------|
| "Security token missing" | CSRF token not found | Refresh page |
| "Please select a quantity" | No quantity selected | Click a quantity button |
| "Product matching query does not exist" | Invalid product ID | Check product exists |
| "An error occurred while adding to cart" | Generic error | Check server logs |
| "403 Forbidden" | CSRF validation failed | Clear cookies, refresh |
| "500 Internal Server Error" | Python error in backend | Check Django logs |

## ✅ Success Indicators

You'll know it's working when:

- ✅ No error alerts appear
- ✅ Success message shows: "Product added to cart successfully!"
- ✅ Cart count in header increases
- ✅ Cart total is displayed
- ✅ No errors in browser console
- ✅ No errors in Django logs

## 🎉 Next Steps After Fix

Once add to cart is working:

1. Go to `/cart/` to see your items
2. Update the cart.html template (see QUICK_START_CART.md)
3. Test quantity updates
4. Test remove from cart
5. Test checkout flow

---

**The fixes have been applied. Please refresh the page and try again!**
