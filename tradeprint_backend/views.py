from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Category, User,SubCategory,SubSubCategory, Product, Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal



from .forms import CategoryForm, SubCategoryForm, SubSubCategoryForm, ProductForm
from django.contrib.auth.decorators import login_required
import json

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        role = request.POST.get('role') 

        if password != cpassword:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        messages.success(request, "Account created successfully!")
        return redirect("signin")

    return render(request, "backend/sign-up.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print(user)
        if user:
            login(request, user)

            # Redirect based on user role
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "shopkeeper":
                return redirect("shop_dashboard")
            else:
                return redirect("user_dashboard")

        messages.error(request, "Invalid email or password")
        return redirect("signin")

    return render(request, "backend/sign-in.html")


def signout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("signin")


@login_required
def admin_dashboard(request):
    if request.user.role == 'shopkeeper':
        return redirect('shop_dashboard')
    
    from django.db.models import Sum
    from .models import Order, User, Product
    from django.utils import timezone
    
    # Statistics
    total_users = User.objects.filter(role='user').count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_products = Product.objects.count()
    
    # Recent Data
    recent_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]
    new_customers = User.objects.filter(role='user').order_by('-date_joined')[:5]
    
    # Calculate daily signups/visits (mocked or real if tracking exists)
    # daily_signups = User.objects.filter(date_joined__date=timezone.now().date()).count()
    
    # --- Chart Data Calculation ---
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    from datetime import timedelta
    
    # 1. Sales Report (Last 7 Days)
    today = timezone.now().date()
    last_7_days = today - timedelta(days=6)
    
    sales_data = Order.objects.filter(created_at__date__gte=last_7_days)\
        .annotate(date=TruncDate('created_at'))\
        .values('date')\
        .annotate(total_sales=Sum('total'))\
        .order_by('date')
        
    # Prepare data for Chart.js
    chart_dates = []
    chart_sales = []
    
    # Fill in missing days
    current_date = last_7_days
    sales_dict = {item['date']: item['total_sales'] for item in sales_data}
    
    while current_date <= today:
        chart_dates.append(current_date.strftime('%d %b')) # e.g., "01 Jan"
        chart_sales.append(float(sales_dict.get(current_date, 0)))
        current_date += timedelta(days=1)
        
    # 2. Orders Overview (Status Breakdown)
    # Statuses: pending, processing, shipped, delivered, cancelled
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_dict = {item['status']: item['count'] for item in status_counts}
    
    # Mapping to chart segments (Completed, Unpaid/Failed, Returned/Refunded, Pending, Canceled)
    # We will adapt the chart to show: Delivered, Shipped, Processing, Pending, Cancelled
    
    doughnut_data = [
        status_dict.get('delivered', 0),    # Completed (Delivered)
        status_dict.get('shipped', 0),      # Shipped
        status_dict.get('processing', 0),   # Processing
        status_dict.get('pending', 0),      # Pending
        status_dict.get('cancelled', 0),    # Cancelled
        status_dict.get('refunded', 0),     # Returned (Refunded)
    ]
    
    print(f"Chart Dates: {chart_dates}")
    print(f"Chart Sales: {chart_sales}")
    print(f"Doughnut Data: {doughnut_data}")

    import json
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'new_customers': new_customers,
        # Chart Data
        'chart_dates': json.dumps(chart_dates),
        'chart_sales': json.dumps(chart_sales),
        'doughnut_data': json.dumps(doughnut_data),
    }
    return render(request, "backend/index.html", context)


@login_required
def shop_dashboard(request):
    if request.user.role != 'shopkeeper':
        messages.error(request, 'Access denied.')
        return redirect('signin')
        
    # Get the shop profile associated with the user
    try:
        shop = request.user.print_shop_profile
        assigned_orders = shop.assigned_orders.select_related('customer').all().order_by('-created_at')
        
        # Stats
        total_assigned = assigned_orders.count()
        pending_orders = assigned_orders.filter(status__in=['pending', 'processing']).count()
        completed_orders = assigned_orders.filter(status__in=['shipped', 'delivered']).count()
        
    except Exception:
        shop = None
        assigned_orders = []
        total_assigned = 0
        pending_orders = 0
        completed_orders = 0
        
    context = {
        'shop': shop,
        'orders': assigned_orders,
        'total_assigned': total_assigned,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    }
    return render(request, "backend/shopkeeper-dashboard.html", context)


@login_required
def user_dashboard(request):
    return render(request, "backend/user-dashboard.html")



def category_list(request, pk=None):

    # ---- Edit Mode ----
    if pk:
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        editing = True
    else:
        category = None
        form = CategoryForm()
        editing = False

    # ---- Handle Form Submit ----
    if request.method == "POST":
        if category:
            form = CategoryForm(request.POST, instance=category)
        else:
            form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("category_list")

    categories = Category.objects.all()

    return render(request, "backend/main-category.html", {
        "categories": categories,
        "form": form,
        "editing": editing,
        "item": category,
    })

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("category_list")

def subcategory_list(request, pk=None):
    # if pk exists → edit mode
    if pk:
        item = get_object_or_404(SubCategory, pk=pk)
        form = SubCategoryForm(instance=item)
        editing = True  
    else:
        item = None
        form = SubCategoryForm()
        editing = False

    # HANDLE FORM SUBMIT
    if request.method == "POST":
        print("POST request received")
        print("POST data:", request.POST)
        
        if item:     # edit mode
            form = SubCategoryForm(request.POST, instance=item)
        else:        # add mode
            form = SubCategoryForm(request.POST)

        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
            
        if form.is_valid():
            try:
                saved_item = form.save()
                print(f"Subcategory saved: {saved_item}")
                if editing:
                    messages.success(request, "Subcategory updated successfully!")
                else:
                    messages.success(request, "Subcategory added successfully!")
                return redirect("subcategory_list")
            except Exception as e:
                print(f"Error saving: {e}")
                messages.error(request, f"Error saving subcategory: {str(e)}")
        else:
            # Show error message if form is invalid
            messages.error(request, "Please correct the errors below.")

    subcategories = SubCategory.objects.select_related("category").all()

    return render(request, "backend/sub-category.html", {
        "form": form,
        "subcategories": subcategories,
        "editing": editing,
        "item": item,
    })

def subcategory_delete(request, pk):
    subcategory = get_object_or_404(SubCategory, pk=pk)
    subcategory.delete()
    return redirect("subcategory_list")

def subsubcategory_list(request, pk=None):

    # -----------------------
    # EDIT MODE
    # -----------------------
    if pk:
        item = get_object_or_404(SubSubCategory, pk=pk)
        form = SubSubCategoryForm(instance=item)
        editing = True
    else:
        item = None
        form = SubSubCategoryForm()
        editing = False

    # -----------------------
    # FORM SUBMISSION
    # -----------------------
    if request.method == "POST":
        print("POST request received for SubSubCategory")
        print("POST data:", request.POST)
        
        if item:
            form = SubSubCategoryForm(request.POST, instance=item)
        else:
            form = SubSubCategoryForm(request.POST)

        print("Form is valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
            
        if form.is_valid():
            try:
                saved_item = form.save()
                print(f"Sub-Subcategory saved: {saved_item}")
                if editing:
                    messages.success(request, "Sub-Subcategory updated successfully!")
                else:
                    messages.success(request, "Sub-Subcategory added successfully!")
                return redirect("subsubcategory_list")
            except Exception as e:
                print(f"Error saving: {e}")
                messages.error(request, f"Error saving sub-subcategory: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")

    # -----------------------
    # TABLE LIST DATA
    # -----------------------
    items = SubSubCategory.objects.select_related(
        "parent_category", "sub_category"
    ).all()

    return render(request, "backend/subsubcategory.html", {
        "form": form,
        "items": items,
        "editing": editing,
        "item": item,
    })

def subsubcategory_delete(request, pk):
    item = get_object_or_404(SubSubCategory, pk=pk)
    item.delete()
    return redirect("subsubcategory_list")


def product_grid(request):
    products = Product.objects.all()
    return render(request, "backend/product-grid.html", {"products": products})

def product_list(request):
    products = Product.objects.all()
    return render(request, "backend/product-list.html", {"products": products})

def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=False)
            
            # Parse material options
            material_text = form.cleaned_data.get('material_options_text', '')
            if material_text:
                material_options = []
                for item in material_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            material_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.material_options = material_options
            
            # Parse size options
            size_text = form.cleaned_data.get('size_options_text', '')
            if size_text:
                size_options = []
                for item in size_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            size_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.size_options = size_options
            
            # Parse lamination options
            lamination_text = form.cleaned_data.get('lamination_options_text', '')
            if lamination_text:
                lamination_options = []
                for item in lamination_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            lamination_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.lamination_options = lamination_options
            
            # Parse banding options
            banding_text = form.cleaned_data.get('banding_options_text', '')
            if banding_text:
                banding_options = []
                for item in banding_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            banding_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.banding_options = banding_options
            
            # Parse quantity tiers from JSON
            quantity_json = request.POST.get('quantity_tiers_json', '[]')
            if quantity_json and quantity_json != '[]':
                try:
                    quantity_tiers = json.loads(quantity_json)
                    product.quantity_tiers = quantity_tiers
                    print(f"Quantity tiers saved: {quantity_tiers}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing quantity tiers JSON: {e}")
            
            # Parse delivery options
            delivery_text = form.cleaned_data.get('delivery_options_text', '')
            if delivery_text:
                delivery_options = []
                for item in delivery_text.split(','):
                    item = item.strip()
                    if '|' in item:
                        parts = item.split('|')
                        if len(parts) == 3:
                            try:
                                delivery_options.append({
                                    "name": parts[0].strip(),
                                    "days": parts[1].strip(),
                                    "price": float(parts[2].strip())
                                })
                            except ValueError:
                                pass
                product.delivery_options = delivery_options
            
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect("product_list")
    else:
        form = ProductForm()
    
    return render(request, "backend/product-add.html", {
        "form": form,
        "editing": False,
        "quantity_tiers_json": '[]'
    })

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            product = form.save(commit=False)
            
            # Parse material options
            material_text = form.cleaned_data.get('material_options_text', '')
            if material_text:
                material_options = []
                for item in material_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            material_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.material_options = material_options
            
            # Parse size options
            size_text = form.cleaned_data.get('size_options_text', '')
            if size_text:
                size_options = []
                for item in size_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            size_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.size_options = size_options
            
            # Parse lamination options
            lamination_text = form.cleaned_data.get('lamination_options_text', '')
            if lamination_text:
                lamination_options = []
                for item in lamination_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            lamination_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.lamination_options = lamination_options
            
            # Parse banding options
            banding_text = form.cleaned_data.get('banding_options_text', '')
            if banding_text:
                banding_options = []
                for item in banding_text.split(','):
                    item = item.strip()
                    if ':' in item:
                        name, price = item.rsplit(':', 1)
                        try:
                            banding_options.append({
                                "name": name.strip(),
                                "price_modifier": float(price.strip())
                            })
                        except ValueError:
                            pass
                product.banding_options = banding_options
            
            # Parse quantity tiers from JSON
            quantity_json = request.POST.get('quantity_tiers_json', '[]')
            if quantity_json and quantity_json != '[]':
                try:
                    quantity_tiers = json.loads(quantity_json)
                    product.quantity_tiers = quantity_tiers
                    print(f"Quantity tiers updated: {quantity_tiers}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing quantity tiers JSON: {e}")
            
            # Parse delivery options
            delivery_text = form.cleaned_data.get('delivery_options_text', '')
            if delivery_text:
                delivery_options = []
                for item in delivery_text.split(','):
                    item = item.strip()
                    if '|' in item:
                        parts = item.split('|')
                        if len(parts) == 3:
                            try:
                                delivery_options.append({
                                    "name": parts[0].strip(),
                                    "days": parts[1].strip(),
                                    "price": float(parts[2].strip())
                                })
                            except ValueError:
                                pass
                product.delivery_options = delivery_options
            
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        # Pre-populate JSON fields as text
        initial_data = {}
        
        if product.material_options:
            initial_data['material_options_text'] = ', '.join([
                f"{opt['name']}:{opt['price_modifier']}" for opt in product.material_options
            ])
        
        if product.size_options:
            initial_data['size_options_text'] = ', '.join([
                f"{opt['name']}:{opt['price_modifier']}" for opt in product.size_options
            ])
        
        if product.lamination_options:
            initial_data['lamination_options_text'] = ', '.join([
                f"{opt['name']}:{opt['price_modifier']}" for opt in product.lamination_options
            ])
        
        if product.banding_options:
            initial_data['banding_options_text'] = ', '.join([
                f"{opt['name']}:{opt['price_modifier']}" for opt in product.banding_options
            ])
        
        if product.delivery_options:
            initial_data['delivery_options_text'] = ', '.join([
                f"{opt['name']}|{opt['days']}|{opt['price']}" for opt in product.delivery_options
            ])
        
        form = ProductForm(instance=product, initial=initial_data)
    
    # Serialize quantity_tiers to JSON for the template
    quantity_tiers_json = json.dumps(product.quantity_tiers) if product.quantity_tiers else '[]'
    
    return render(request, "backend/product-add.html", {
        "form": form, 
        "editing": True, 
        "product": product,
        "quantity_tiers_json": quantity_tiers_json
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "backend/product-detail.html", {"product": product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("product_list")


# ========================================
# CART FUNCTIONALITY
# ========================================

def get_or_create_cart(request):
    """Get or create a cart for the current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # For anonymous users, use session
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


@require_POST
def add_to_cart(request):
    """Add a product to the cart with configuration"""
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        material = request.POST.get('material', '')
        size = request.POST.get('size', '')
        sides_printed = request.POST.get('sides_printed', '')
        lamination = request.POST.get('lamination', '')
        banding = request.POST.get('banding', '')
        delivery_service = request.POST.get('delivery_service', 'Standard')
        delivery_days = request.POST.get('delivery_days', '')
        # Clean price strings
        unit_price_str = request.POST.get('unit_price', '0').replace('£', '').replace(',', '').strip()
        if not unit_price_str: unit_price_str = '0'
        unit_price = Decimal(unit_price_str)

        delivery_price_str = request.POST.get('delivery_price', '0').replace('£', '').replace(',', '').strip()
        if not delivery_price_str: delivery_price_str = '0'
        delivery_price = Decimal(delivery_price_str)

        product = get_object_or_404(Product, pk=product_id)
        cart = get_or_create_cart(request)

        # Check if same configuration already exists in cart
        existing_item = cart.items.filter(
            product=product,
            material=material,
            size=size,
            sides_printed=sides_printed,
            lamination=lamination,
            banding=banding,
            delivery_service=delivery_service
        ).first()

        if existing_item:
            # Update quantity if same configuration exists
            existing_item.quantity = quantity
            existing_item.unit_price = unit_price
            existing_item.delivery_price = delivery_price
            existing_item.save()
            message = "Cart updated successfully!"
        else:
            # Create new cart item
            CartItem.objects.create(
                cart=cart,
                product=product,
                material=material,
                size=size,
                sides_printed=sides_printed,
                lamination=lamination,
                banding=banding,
                quantity=quantity,
                delivery_service=delivery_service,
                delivery_days=delivery_days,
                unit_price=unit_price,
                delivery_price=delivery_price
            )
            message = "Product added to cart successfully!"

        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart.total_items,
            'cart_total': float(cart.total)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


def view_cart(request):
    """View cart page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': cart.subtotal,
        'vat': cart.vat,
        'total': cart.total
    }
    return render(request, 'frontend/cart.html', context)


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Cart updated successfully!',
                'item_total': float(cart_item.total_price),
                'cart_subtotal': float(cart.subtotal),
                'cart_vat': float(cart.vat),
                'cart_total': float(cart.total),
                'cart_count': cart.total_items
            })
        else:
            cart_item.delete()
            return JsonResponse({
                'success': True,
                'message': 'Item removed from cart',
                'cart_subtotal': float(cart.subtotal),
                'cart_vat': float(cart.vat),
                'cart_total': float(cart.total),
                'cart_count': cart.total_items
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
        cart_item.delete()
        
        messages.success(request, 'Item removed from cart successfully!')
        return redirect('view_cart')
        
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
        return redirect('view_cart')


def get_cart_count(request):
    """API endpoint to get cart count"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'count': cart.total_items,
        'subtotal': float(cart.subtotal),
        'total': float(cart.total)
    })


def checkout(request):
    """Checkout page"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': cart.subtotal,
        'vat': cart.vat,
        'total': cart.total
    }
    return render(request, 'frontend/checkout.html', context)


# ========================================
# USER MANAGEMENT (Admin)
# ========================================

@login_required
def user_list(request):
    """Display list of regular users (role='user') for admin"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('admin_dashboard')
    
    # Only show users with role='user', exclude admins and shopkeepers
    users = User.objects.select_related('customer_profile').filter(role='user').order_by('-date_joined')
    
    context = {
        'users': users
    }
    return render(request, 'backend/user-management.html', context)


@login_required
def user_detail(request, user_id):
    """Get user details as JSON"""
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    user = get_object_or_404(User, pk=user_id)
    
    data = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role,
        'is_active': user.is_active,
        'date_joined': user.date_joined.strftime('%B %d, %Y'),
        'last_login': user.last_login.strftime('%B %d, %Y %I:%M %p') if user.last_login else None,
    }
    
    # Add customer profile data if exists
    if hasattr(user, 'customer_profile') and user.customer_profile:
        profile = user.customer_profile
        data.update({
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'postcode': profile.postcode,
            'state': profile.state,
            'country': profile.country,
        })
    else:
        data['phone'] = None
    
    return JsonResponse(data)


@login_required
def user_add(request):
    """Add a new user"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('user_add')
        
        try:
            # Create User
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.role = role
            user.save()
            
            # Create optional customer profile
            if role == 'user':
                Customer.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    # Other fields empty for now
                )
            
            messages.success(request, 'User added successfully!')
            return redirect('user_list')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('user_add')
            
    return render(request, 'backend/user-add.html')


@login_required
def user_edit(request, user_id):
    """Edit user details"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('admin_dashboard')
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')
    
    context = {
        'user_obj': user
    }
    return render(request, 'backend/user-edit.html', context)


@login_required
@require_POST
def user_delete(request, user_id):
    """Delete a user"""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        user = get_object_or_404(User, pk=user_id)
        
        # Prevent deleting superuser
        if user.is_superuser:
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete superuser account'
            }, status=400)
        
        # Prevent self-deletion
        if user.id == request.user.id:
            return JsonResponse({
                'success': False,
                'error': 'Cannot delete your own account'
            }, status=400)
        
        user.delete()
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# ========================================
# ORDER MANAGEMENT (Admin)
# ========================================

@login_required
def order_list(request):
    """Display list of orders"""
    # Allow admin and shopkeeper
    if request.user.role not in ['admin', 'shopkeeper']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user_dashboard')
    
    from .models import Order, PrintShop
    
    print_shops = []
    if request.user.role == 'shopkeeper':
        # Shopkeeper sees only assigned orders
        try:
            shop = request.user.print_shop_profile
            orders = shop.assigned_orders.select_related('customer', 'user', 'assigned_shop').order_by('-created_at')
        except Exception:
            orders = Order.objects.none()
    else:
        # Admin sees all orders
        orders = Order.objects.select_related('customer', 'user', 'assigned_shop').all().order_by('-created_at')
        # Get active shops for manual assignment (ensure they are valid shopkeepers)
        print_shops = PrintShop.objects.filter(status='active', user__role='shopkeeper').order_by('shop_name')
    
    context = {
        'orders': orders,
        'print_shops': print_shops
    }
    return render(request, 'backend/order-list.html', context)


@login_required
def order_detail(request, order_id):
    """View order details"""
    from .models import Order
    
    order = get_object_or_404(Order, pk=order_id)
    
    # Check permissions
    if request.user.role == 'shopkeeper':
        # Ensure order is assigned to this shop
        if not hasattr(request.user, 'print_shop_profile') or order.assigned_shop != request.user.print_shop_profile:
             messages.error(request, 'Access denied.')
             return redirect('shop_dashboard')
    elif request.user.role != 'admin':
         messages.error(request, 'Access denied.')
         return redirect('user_dashboard')
    
    # Ensure barcode exists
    if not order.barcode_image:
        order.save()
        
    order_items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'backend/order-detail.html', context)


@login_required
def order_update_status(request, order_id):
    """Update order status"""
    if request.user.role not in ['admin', 'shopkeeper']:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    if request.method == 'POST':
        from .models import Order
        
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                 return JsonResponse({'success': True})
            
            messages.success(request, f'Order status updated to {order.get_status_display()}')
            return redirect('order_detail', order_id=order.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
            messages.error(request, 'Invalid status')
            return redirect('order_detail', order_id=order.id)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def validate_artwork(request, order_id):
    """Validate artwork for an order"""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('admin_dashboard')
    
    from .models import Order
    order = get_object_or_404(Order, pk=order_id)
    
    order.is_artwork_verified = True
    order.save()
    
    messages.success(request, f'Artwork for Order {order.order_number} verified successfully.')
    return redirect('order_detail', order_id=order.id)

@login_required
def send_order_to_printer(request, order_id):
    """Send order details to printing shop (simulated)"""
    if request.user.role not in ['admin', 'shopkeeper']:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('admin_dashboard')
    
    from .models import Order
    order = get_object_or_404(Order, pk=order_id)
    
    # Simulate sending email or API call
    # In reality, this would trigger an email with the generated barcode
    if not order.barcode_image:
        order.save() # This triggers barcode generation
        
    order.is_sent_to_printer = True
    if order.status == 'pending':
        order.status = 'processing'
    order.save()
    
    messages.success(request, f'Order {order.order_number} sent to printing shop successfully.')
    return redirect('order_detail', order_id=order.id)


@login_required
def integrate_delivery(request, order_id):
    """
    Simulate integration with a delivery partner api.
    Generates a mock tracking number and label.
    """
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('order_detail', order_id=order_id)
        
    from .models import Order
    order = get_object_or_404(Order, pk=order_id)
    
    # Generate mock data
    import random
    import string
    
    if not order.tracking_number:
        # Mock tracking number: TRK-123456789
        order.tracking_number = f"TRK-{''.join(random.choices(string.digits, k=9))}"
        
        # Mock label URL (in reality this would be a file or external URL)
        # For this demo, we can just point to a placeholder or generate a simple PDF if we had the lib
        # We will use the barcode image as a proxy for the label for now, or a static asset
        order.shipping_label_url = "/static/assets/img/mock_shipping_label.png" 
        
        order.status = 'shipped' # Or 'processing', depending on workflow. Let's say processing until handed over.
        # But usually 'integrate delivery' means label created -> Ready to ship.
        
        order.save()
        messages.success(request, f'Delivery integrated. Tracking: {order.tracking_number}')
    else:
        messages.info(request, 'Delivery already integrated.')
        
    return redirect('order_detail', order_id=order_id)

@login_required
def auto_assign_order(request, order_id):
    """Manually trigger auto-assignment"""
    if request.user.role != 'admin':
        messages.error(request, 'Permission denied.')
        return redirect('order_list')
        
    from .models import Order
    order = get_object_or_404(Order, pk=order_id)
    
    # If force or re-assigning, clear first
    if order.assigned_shop:
        order.assigned_shop = None
        
    # Trigger save to run the model's auto-assign logic
    order.save()
    if order.assigned_shop:
        messages.success(request, f"Order assigned to {order.assigned_shop.shop_name}")
    else:
        messages.warning(request, "No active Print Shops found to assign.")
        
    return redirect('order_list')

@login_required
def assign_order_manual(request, order_id):
    """Manually assign order to a specific shop"""
    if request.user.role != 'admin' or request.method != 'POST':
        messages.error(request, 'Permission denied.')
        return redirect('order_list')
        
    from .models import Order, PrintShop
    
    order = get_object_or_404(Order, pk=order_id)
    shop_id = request.POST.get('shop_id')
    
    if shop_id:
        shop = get_object_or_404(PrintShop, pk=shop_id)
        order.assigned_shop = shop
        order.save()
        messages.success(request, f"Order manually assigned to {shop.shop_name}")
    else:
        messages.error(request, "Please select a shop.")
        
    return redirect('order_list')

# ========================================
# SHOPKEEPER MANAGEMENT
# ========================================

@login_required
def shopkeeper_list(request):
    """List all shopkeepers"""
    if request.user.role != 'admin':
         return redirect('user_dashboard')
         
    from .models import PrintShop
    shops = PrintShop.objects.select_related('user').all()
    context = {'shops': shops}
    return render(request, 'backend/shopkeeper-list.html', context)

@login_required
def shopkeeper_add(request):
    """Add a new shopkeeper user and profile"""
    if request.user.role != 'admin':
         return redirect('user_dashboard')
         
    if request.method == 'POST':
        from .models import User, PrintShop
        
        # Simple form handling
        name = request.POST.get('shop_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('shopkeeper_add')
            
        # Create User
        user = User.objects.create_user(username=email, email=email, password=password)
        user.role = 'shopkeeper'
        user.save()
        
        # Create Shop Profile
        PrintShop.objects.create(
            user=user,
            shop_name=name,
            location=location,
            contact_phone=phone,
            status='active'
        )
        
        messages.success(request, "Shopkeeper added successfully")
        return redirect('shopkeeper_list')
        
    return render(request, 'backend/shopkeeper-add.html')


@login_required
def shopkeeper_edit(request, pk):
    """Edit shopkeeper details"""
    if request.user.role != 'admin':
         return redirect('user_dashboard')

    from .models import PrintShop, User
    
    shop = get_object_or_404(PrintShop, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('shop_name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        status = request.POST.get('status')
        
        # Check if email is being changed and if it duplicates another user
        if email != shop.user.email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('shopkeeper_edit', pk=pk)
        
        # Update User
        shop.user.email = email
        shop.user.username = email  # Keep username same as email
        shop.user.save()
        
        # Update Shop Profile
        shop.shop_name = name
        shop.location = location
        shop.contact_phone = phone
        shop.status = status
        shop.save()
        
        messages.success(request, "Shopkeeper updated successfully")
        return redirect('shopkeeper_list')
        
    return render(request, 'backend/shopkeeper-edit.html', {'shop': shop})


@login_required
def shopkeeper_delete(request, pk):
    """Delete shopkeeper"""
    if request.user.role != 'admin':
         return redirect('user_dashboard')

    from .models import PrintShop
    
    shop = get_object_or_404(PrintShop, pk=pk)
    user = shop.user
    
    # Delete shop first, then user? Or Cascade will handle it.
    # Usually deleting user deletes profile if on_delete=Cascade on OneToOne
    # shop.user is OneToOne.
    
    try:
        user.delete() # This should Cascade delete the shop profile
        messages.success(request, "Shopkeeper deleted successfully")
    except Exception as e:
        messages.error(request, f"Error deleting shopkeeper: {str(e)}")
        
    return redirect('shopkeeper_list')

