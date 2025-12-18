# Product Configuration Order - Tradeprint Style

## Current Order (INCORRECT):
1. Quantity Selection
2. Material Selection  
3. Size Selection
4. Delivery Options

## Correct Order (TRADEPRINT STYLE):
1. **Material Selection** - 350gsm Silk, 300gsm Kraft, 400gsm Uncoated
2. **Size Selection** - 85 x 55mm, 90 x 50mm, A7
3. **Quantity Selection** - 50, 100, 250, 500, 1000, 2500
4. **Delivery Options** - Saver, Standard, Express

## Instructions to Fix:

In the file: `d:\fiverr\Tradeprint_eco\tradeprint_app\templates\frontend\product-full-width.html`

Around lines 382-432, you need to reorder the sections:

### Step 1: Cut the "Quantity Selection" section (lines 382-393)
```html
<!-- Quantity Selection -->
<div class="config-section">
    <label class="config-label">Select Quantity</label>
    <div class="quantity-selector">
        <button class="qty-btn active" onclick="selectQuantity(this, 50)">50</button>
        <button class="qty-btn" onclick="selectQuantity(this, 100)">100</button>
        <button class="qty-btn" onclick="selectQuantity(this, 250)">250</button>
        <button class="qty-btn" onclick="selectQuantity(this, 500)">500</button>
        <button class="qty-btn" onclick="selectQuantity(this, 1000)">1000</button>
        <button class="qty-btn" onclick="selectQuantity(this, 2500)">2500</button>
    </div>
</div>
```

### Step 2: Move it AFTER the "Size Selection" section

### Final Order Should Be:
1. Material Selection (lines 395-403)
2. Size Selection (lines 405-413)  
3. Quantity Selection (move here)
4. Delivery Options (lines 415-432)

This will match the Tradeprint website layout exactly!
