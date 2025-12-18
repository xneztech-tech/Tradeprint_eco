"""
Context processors to make cart data available in all templates
"""
from .models import Cart, CartItem


def cart_context(request):
    """
    Make cart data available in all templates
    This allows the side cart to display on every page
    """
    # Get or create cart for current user/session
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    # Get cart items (limit to 10 for performance)
    cart_items = cart.items.select_related('product').all()[:10]
    
    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_count': cart.total_items,
        'cart_subtotal': cart.subtotal,
        'cart_vat': cart.vat,
        'cart_total': cart.total
    }
