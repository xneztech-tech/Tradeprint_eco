
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from tradeprint_backend.models import Category, SubCategory, SubSubCategory, Product, Cart, CartItem, Order, OrderItem, Customer, User
from decimal import Decimal

def home(req):
    return render(req, 'frontend/home.html')

def frontend_base_context(request):

    categories = Category.objects.filter(status="active").order_by("name")

    menu = []

    for cat in categories:

        # SubCategory: uses "category"
        subcats = SubCategory.objects.filter(category=cat, status="active").order_by("name")

        subcat_block = []
        for sub in subcats:

            # Products: uses "sub_category"
            products = Product.objects.filter(
                sub_category=sub,
                status="active"
            ).order_by("name")

            subcat_block.append({
                "subcategory": sub,
                "products": products
            })

        menu.append({
            "category": cat,
            "subcategories": subcat_block
        })

    # Get cart items for the current user/session
    cart = None
    cart_items = []
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()
    
    if cart:
        cart_items = cart.items.all()

    return {
        "menu_data": menu,
        "cart_items": cart_items,
        "cart": cart
    }

# Category page - shows all products in a category
def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, status='active')
    products = Product.objects.filter(category=category, status='active')
    
    context = {
        'category': category,
        'products': products,
        'page_title': category.name
    }
    return render(request, 'frontend/category.html', context)

# Subcategory page - shows products in a subcategory
def subcategory_view(request, category_slug, subcategory_slug):
    category = get_object_or_404(Category, slug=category_slug, status='active')
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category, status='active')
    products = Product.objects.filter(sub_category=subcategory, status='active')
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
        'page_title': f"{category.name} - {subcategory.name}"
    }
    return render(request, 'frontend/subcategory.html', context)

# Sub-subcategory page - shows products in a sub-subcategory
def subsubcategory_view(request, category_slug, subcategory_slug, subsubcategory_slug):
    category = get_object_or_404(Category, slug=category_slug, status='active')
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category, status='active')
    subsubcategory = get_object_or_404(SubSubCategory, slug=subsubcategory_slug, sub_category=subcategory, status='active')
    products = Product.objects.filter(sub_sub_category=subsubcategory, status='active')
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'subsubcategory': subsubcategory,
        'products': products,
        'page_title': f"{category.name} - {subcategory.name} - {subsubcategory.name}"
    }
    return render(request, 'frontend/subsubcategory.html', context)

# Product detail page
def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, status='active')
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        status='active'
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
        'page_title': product.name
    }
    return render(request, 'frontend/product-full-width.html', context)

def product_full_width(request):
    return render(request, 'frontend/product-full-width.html')

def cart_test(request):
    """Test page for cart functionality"""
    return render(request, 'frontend/cart-test.html')

# Cart Views
def get_or_create_cart(request):
    """Get or create cart for user or session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def view_cart(request):
    """Display cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'page_title': 'Shopping Cart'
    }
    return render(request, 'frontend/cart.html', context)

def add_to_cart(request, product_id):
    """Add product to cart"""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            cart = get_or_create_cart(request)
            
            # Get configuration from POST data
            quantity = int(request.POST.get('quantity', 1))
            material = request.POST.get('material', '')
            size = request.POST.get('size', '')
            sides_printed = request.POST.get('sides_printed', '')
            lamination = request.POST.get('lamination', '')
            banding = request.POST.get('banding', '')
            delivery_service = request.POST.get('delivery_service', 'Standard')
            delivery_days = request.POST.get('delivery_days', '')
            # Clean price strings (remove currency symbols and commas)
            unit_price_str = request.POST.get('unit_price', '0').replace('£', '').replace(',', '').strip()
            if not unit_price_str: unit_price_str = '0'
            unit_price = Decimal(unit_price_str)
            
            delivery_price_str = request.POST.get('delivery_price', '0').replace('£', '').replace(',', '').strip()
            if not delivery_price_str: delivery_price_str = '0'
            delivery_price = Decimal(delivery_price_str)
            
            # Get artwork file
            artwork_file = request.FILES.get('artwork')
            
            # Create cart item
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
                material=material,
                size=size,
                sides_printed=sides_printed,
                lamination=lamination,
                banding=banding,
                artwork_file=artwork_file,
                delivery_service=delivery_service,
                delivery_days=delivery_days,
                unit_price=unit_price,
                delivery_price=delivery_price
            )
            
            # Calculate cart total
            cart_total = sum(item.unit_price * item.quantity for item in cart.items.all())
            
            # Return JSON response for AJAX requests
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart!',
                'cart_total': float(cart_total),
                'cart_count': cart.items.count()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart!')
    
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('view_cart')


def get_cart_count(request):
    """Get cart item count as JSON"""
    from django.http import JsonResponse
    
    cart = get_or_create_cart(request)
    count = cart.items.count()
    
    return JsonResponse({'count': count})

def checkout(request):
    """Checkout page and order processing - LOGIN REQUIRED"""
    
    # Check if user is logged in
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to place an order.')
        # Store the redirect URL so we can return after login
        request.session['next'] = '/checkout/'
        return redirect('user_login')  # Redirect to login page
    
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        country = request.POST.get('country')
        state = request.POST.get('state', '')
        delivery_method = request.POST.get('delivery_method', 'standard')
        delivery_notes = request.POST.get('delivery_notes', '')
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Get or create customer
        customer = None
        if request.user.is_authenticated:
            # Try to get existing customer profile
            try:
                customer = request.user.customer_profile
            except:
                # Create new customer profile for logged-in user
                customer = Customer.objects.create(
                    user=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    postcode=postcode,
                    country=country,
                    state=state
                )
        else:
            # For guest checkout, try to find existing customer by email
            customer = Customer.objects.filter(email=email, user__isnull=True).first()
            if not customer:
                # Create new guest customer
                customer = Customer.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    address=address,
                    city=city,
                    postcode=postcode,
                    country=country,
                    state=state
                )
        
        # Calculate totals
        subtotal = cart.subtotal
        vat = cart.vat
        delivery_charge = Decimal('5.00') if delivery_method == 'express' else Decimal('0.00')
        total = subtotal + vat + delivery_charge
        
        # Create the order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            customer=customer,
            shipping_first_name=first_name,
            shipping_last_name=last_name,
            shipping_email=email,
            shipping_phone=phone,
            shipping_address=address,
            shipping_city=city,
            shipping_postcode=postcode,
            shipping_country=country,
            shipping_state=state,
            delivery_method=delivery_method,
            delivery_notes=delivery_notes,
            payment_method=payment_method,
            payment_status='paid' if payment_method != 'cod' else 'pending',
            subtotal=subtotal,
            vat=vat,
            delivery_charge=delivery_charge,
            total=total,
            status='pending'
        )
        
        # Create order items from cart items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                material=cart_item.material,
                size=cart_item.size,
                sides_printed=cart_item.sides_printed,
                lamination=cart_item.lamination,
                banding=cart_item.banding,
                artwork_file=cart_item.artwork_file,
                quantity=cart_item.quantity,
                delivery_service=cart_item.delivery_service,
                delivery_days=cart_item.delivery_days,
                unit_price=cart_item.unit_price,
                delivery_price=cart_item.delivery_price,
                total_price=cart_item.total_price
            )
        
        # Clear the cart
        cart_items.delete()
        
        # Success message
        messages.success(request, f'Order placed successfully! Your order number is {order.order_number}')
        
        # Redirect to home
        return redirect('home')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'page_title': 'Checkout'
    }
    return render(request, 'frontend/checkout.html', context)


# ========================================
# USER REGISTRATION (Frontend)
# ========================================

def user_register(request):
    """Frontend user registration"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('user_register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('user_register')
        
        try:
            # Create user account
            username = email.split('@')[0]  # Use email prefix as username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='user'  # Default role for frontend registration
            )
            
            # Create customer profile
            Customer.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            
            # Log the user in
            login(request, user)
            
            messages.success(request, 'Account created successfully! Welcome to Tradeprint!')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('user_register')
    
    return render(request, 'frontend/register-user.html')


def user_login(request):
    """Frontend user login"""
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login as auth_login
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Check if user is a regular customer (not admin/shopkeeper)
            if user.role == 'user':
                auth_login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect to checkout if that's where they came from
                next_url = request.session.get('next', '/home/')
                if 'next' in request.session:
                    del request.session['next']
                return redirect(next_url)
            else:
                messages.error(request, 'Please use the admin login page.')
                return redirect('user_login')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('user_login')
    
    return render(request, 'frontend/user-login.html')


def user_logout(request):
    """Frontend user logout"""
    from django.contrib.auth import logout
    
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


def my_orders(request):
    """Customer order list - shows user's own orders"""
    from django.contrib.auth.decorators import login_required
    
    # Require login
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view your orders.')
        return redirect('user_login')
    
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
        'page_title': 'My Orders'
    }
    
    return render(request, 'frontend/my-orders.html', context)


def order_detail(request, order_id):
    """Customer order detail - shows single order details"""
    
    # Require login
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view order details.')
        return redirect('user_login')
    
    # Get order and verify it belongs to the user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'page_title': f'Order #{order.order_number}'
    }
    
    return render(request, 'frontend/order-detail.html', context)

# ========================================
# PASSWORD RESET FUNCTIONALITY
# ========================================

def forgot_password(request):
    """Forgot password - send reset email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email, role='user')
            
            # Generate password reset token
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.core.mail import send_mail
            from django.conf import settings
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Build reset URL
            reset_url = request.build_absolute_uri(
                f'/reset-password/{uid}/{token}/'
            )
            
            # Send email
            subject = 'Password Reset Request - Tradeprint'
            message = f"""
Hello {user.first_name},

You requested to reset your password. Click the link below to reset your password:

{reset_url}

If you didn't request this, please ignore this email.

This link will expire in 24 hours.

Best regards,
Tradeprint Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('password_reset_sent')
            except Exception as e:
                # If email fails, still show success page for security
                # (don't reveal if email exists)
                messages.info(request, 'If an account exists with this email, you will receive a password reset link.')
                return redirect('password_reset_sent')
                
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            messages.info(request, 'If an account exists with this email, you will receive a password reset link.')
            return redirect('password_reset_sent')
    
    return render(request, 'frontend/forgot-password.html')


def password_reset_sent(request):
    """Password reset email sent confirmation"""
    return render(request, 'frontend/password-reset-sent.html')


def reset_password(request, uidb64, token):
    """Reset password with token"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return render(request, 'frontend/reset-password.html')
            
            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters long!')
                return render(request, 'frontend/reset-password.html')
            
            # Set new password
            user.set_password(password)
            user.save()
            
            messages.success(request, 'Password reset successful! You can now login with your new password.')
            return redirect('user_login')
        
        return render(request, 'frontend/reset-password.html')
    else:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('forgot_password')


def contact_us(request):
    """Contact Us Page"""
    return render(request, 'frontend/contact-us.html')

def help_page(request):
    """Help / FAQ Page"""
    return render(request, 'frontend/faq.html')
