<script>
function changeImage(thumbnail) {
    document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
    thumbnail.classList.add('active');
    document.getElementById('mainImage').src = thumbnail.src;
}

function selectQuantity(btn, quantity) {
    document.querySelectorAll('.qty-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    updatePrice();
}

function selectOption(btn) {
    const siblings = btn.parentElement.querySelectorAll('.option-btn');
    siblings.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    updatePrice();
}

function selectDelivery(card) {
    document.querySelectorAll('.delivery-card').forEach(c => c.classList.remove('active'));
    card.classList.add('active');
    updatePrice();
}

function updatePrice() {
    const selectedQty = document.querySelector('.qty-btn.active');
    const selectedDelivery = document.querySelector('.delivery-card.active');

    if (selectedQty && selectedDelivery) {
        let price = 0;
        const deliveryName = selectedDelivery.querySelector('.delivery-name').textContent.trim();

        if (deliveryName.includes('Saver')) {
            price = parseFloat(selectedQty.dataset.saver || 0);
        } else if (deliveryName.includes('Express')) {
            price = parseFloat(selectedQty.dataset.express || 0);
        } else {
            price = parseFloat(selectedQty.dataset.standard || 0);
        }

        const priceElement = document.getElementById('currentPrice');
        if (priceElement && price > 0) {
            priceElement.textContent = '£' + price.toFixed(2);
        }
    }
}

function showTab(index) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

    document.querySelectorAll('.tab-content')[index].classList.add('active');
    document.querySelectorAll('.tab-btn')[index].classList.add('active');
}

function addToCart() {
    const quantity = document.querySelector('.qty-btn.active')?.textContent || 'Not selected';
    const material = document.querySelector('.option-btn.active')?.textContent || 'Not selected';
    const size = document.querySelectorAll('.config-section')[1]?.querySelector('.option-btn.active')?.textContent || 'Not selected';
    const delivery = document.querySelector('.delivery-card.active')?.querySelector('.delivery-name')?.textContent || 'Not selected';
    const price = document.getElementById('currentPrice').textContent;

    alert(`Added to cart:\nMaterial: ${material}\nSize: ${size}\nQuantity: ${quantity}\nDelivery: ${delivery}\nPrice: ${price}`);
}

// Initialize price on page load
document.addEventListener('DOMContentLoaded', function () {
    updatePrice();
});
</script>
