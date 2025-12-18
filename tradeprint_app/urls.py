from django.urls import path
from . import views



urlpatterns = [
    path('home/', views.home, name="home"),

    # path("signup/", views.signup, name="signup"),
    # path("signin/", views.signin, name="signin"),
    
    # Category pages
    path('category/<slug:category_slug>/', views.category_view, name="category"),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_view, name="subcategory"),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/<slug:subsubcategory_slug>/', views.subsubcategory_view, name="subsubcategory"),
    
    # Product detail
    path('product/<int:product_id>/', views.product_detail_view, name="product_detail"),
    path('product-full-width/', views.product_full_width, name="product_full_width"),
    
    # Cart
    path('cart/', views.view_cart, name="view_cart"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/update/<int:item_id>/', views.update_cart_item, name="update_cart_item"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/count/', views.get_cart_count, name="get_cart_count"),
    path('checkout/', views.checkout, name="checkout"),
    
    # User Registration & Login
    path('register/', views.user_register, name="user_register"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    
    # Customer Orders
    path('my-orders/', views.my_orders, name="my_orders"),
    path('order/<int:order_id>/', views.order_detail, name="order_detail_customer"),
    
    # Test page
    path('cart-test/', views.cart_test, name="cart_test"),
    
    # Static Info Pages
    path('contact-us/', views.contact_us, name="contact_us"),
    path('help/', views.help_page, name="help_page"),
    path('faq/', views.help_page, name="faq"), # Alias for help
]