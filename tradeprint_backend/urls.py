from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("shop-dashboard/", views.shop_dashboard, name="shop_dashboard"),
    path("shopkeeper/add/", views.shopkeeper_add, name="shopkeeper_add"),
    path("shopkeeper/list/", views.shopkeeper_list, name="shopkeeper_list"),
    path("shopkeeper/edit/<int:pk>/", views.shopkeeper_edit, name="shopkeeper_edit"),
    path("shopkeeper/delete/<int:pk>/", views.shopkeeper_delete, name="shopkeeper_delete"),
    path("shopkeeper/fix-profiles/", views.fix_shopkeeper_profiles, name="fix_shopkeeper_profiles"),
    path("user-dashboard/", views.user_dashboard, name="user_dashboard"),
    
    # ==========================
    # MAIN CATEGORY CRUD
    # ==========================
    
    path("main-category/", views.category_list, name="category_list"),
    path("main-category/edit/<int:pk>/", views.category_list, name="category_edit"),
    path("main-category/delete/<int:pk>/", views.category_delete, name="category_delete"),
    
    # ==========================
    # SUB CATEGORY CRUD
    # ==========================
    path("sub-category/", views.subcategory_list, name="subcategory_list"),
    path("sub-category/edit/<int:pk>/", views.subcategory_list, name="subcategory_edit"),
    path("sub-category/delete/<int:pk>/", views.subcategory_delete, name="subcategory_delete"),
    
    # SUB-SUBCATEGORY
    path("sub-sub-category/", views.subsubcategory_list, name="subsubcategory_list"),
    path("sub-sub-category/edit/<int:pk>/", views.subsubcategory_list, name="subsubcategory_edit"),
    path("sub-sub-category/delete/<int:pk>/", views.subsubcategory_delete, name="subsubcategory_delete"),
    
    # PRODUCT
    path("product-grid/", views.product_grid, name="product_grid"),
    path("product-list/", views.product_list, name="product_list"),
    path("product-add/", views.product_add, name="product_add"),
    path("product-edit/<int:pk>/", views.product_edit, name="product_edit"),
    path("product-detail/<int:pk>/", views.product_detail, name="product_detail"),
    path("product-delete/<int:pk>/", views.product_delete, name="product_delete"),
    
    # USER MANAGEMENT
    path("users/", views.user_list, name="user_list"),
    path("user-add/", views.user_add, name="user_add"),
    path("user-detail/<int:user_id>/", views.user_detail, name="user_detail"),
    path("user-edit/<int:user_id>/", views.user_edit, name="user_edit"),
    path("user-delete/<int:user_id>/", views.user_delete, name="user_delete"),
    
    # ORDER MANAGEMENT
    path("orders/", views.order_list, name="order_list"),
    path("order-detail/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order-update-status/<int:order_id>/", views.order_update_status, name="order_update_status"),
    path("order-validate-artwork/<int:order_id>/", views.validate_artwork, name="validate_artwork"),
    path("order-send-printer/<int:order_id>/", views.send_order_to_printer, name="send_order_to_printer"),
    path("order-integrate-delivery/<int:order_id>/", views.integrate_delivery, name="integrate_delivery"),
    path("order-auto-assign/<int:order_id>/", views.auto_assign_order, name="auto_assign_order"),
    path("order-manual-assign/<int:order_id>/", views.assign_order_manual, name="assign_order_manual"),
    
]
