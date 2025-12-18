from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Category,SubCategory,SubSubCategory

class CustomUserAdmin(BaseUserAdmin):

    model = User

    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('User Role', {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)

# -------------------------------
# SubCategory Inline (inside Category admin)
# -------------------------------
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    min_num = 0
    max_num = 20
    show_change_link = True
    
class SubSubCategoryInline(admin.TabularInline):
    model = SubSubCategory
    extra = 1
    show_change_link = True
# -------------------------------
# Category Admin
# -------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "trending", "slug")
    search_fields = ("name", "slug", "tags")
    list_filter = ("status", "trending")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]
    ordering = ("name",)
    
    
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "status", "trending")
    search_fields = ("name", "category__name")
    list_filter = ("category", "status", "trending")
    ordering = ("category", "name")
    prepopulated_fields = {"slug": ("name",)}



# -------------------------
# SUB-SUBCATEGORY ADMIN (LEVEL 3)
# -------------------------

@admin.register(SubSubCategory)
class SubSubCategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "parent_category", "sub_category", "status", "trending", "slug")
    search_fields = ("name", "slug", "parent_category__name", "sub_category__name")
    list_filter = ("status", "trending", "parent_category", "sub_category")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("parent_category", "sub_category", "name")