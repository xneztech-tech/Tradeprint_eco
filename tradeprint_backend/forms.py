from django import forms
from .models import Category, SubCategory, SubSubCategory, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "short_description",
            "full_description",
            "tags",
            "status",
            "trending",
        ]
        
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = [
            "category",
            "name",
            "slug",
            "short_description",
            "full_description",
            "tags",
            "status",
            "trending",
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control slug-title', 'required': True}),
            'slug': forms.TextInput(attrs={'class': 'form-control set-slug'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'trending': forms.Select(attrs={'class': 'form-control'}),
        }

class SubSubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubSubCategory
        fields = [
            "parent_category",
            "sub_category",
            "name",
            "slug",
            "short_description",
            "full_description",
            "tags",
            "status",
            "trending",
        ]
        widgets = {
            'parent_category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'sub_category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control slug-title', 'required': True}),
            'slug': forms.TextInput(attrs={'class': 'form-control set-slug'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'trending': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    # Text fields for JSON data (will be converted to JSON in view)
    material_options_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., 130gsm Gloss:0, 170gsm Matt:5'
        }),
        required=False,
        help_text="Format: Name:PriceModifier, separated by commas"
    )
    size_options_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., A5:0, A4:10, A3:20'
        }),
        required=False,
        help_text="Format: Name:PriceModifier, separated by commas"
    )
    lamination_options_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., None:0, Matt:15, Gloss:15'
        }),
        required=False,
        help_text="Format: Name:PriceModifier, separated by commas"
    )
    banding_options_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., None:0, 50s:5, 100s:8'
        }),
        required=False,
        help_text="Format: Name:PriceModifier, separated by commas"
    )
    quantity_tiers_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., 100:50, 500:200, 1000:350'
        }),
        required=False,
        help_text="Format: Quantity:Price, separated by commas"
    )
    delivery_options_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control',
            'placeholder': 'e.g., Saver|5-7|0, Standard|3-5|10, Express|1-2|25'
        }),
        required=False,
        help_text="Format: Name|Days|Price, separated by commas"
    )
    
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'sub_category', 'sub_sub_category',
            'short_description', 'full_description', 'tags',
            'base_price', 'sides_printed', 'double_sided_price',
            'allow_different_designs', 'max_different_designs',
            'main_image', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6',
            'stock_quantity', 'min_order_quantity', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter product name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'auto-generated-slug'}),
            'category': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'sub_category': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'sub_sub_category': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'short_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Brief description of the product'}),
            'full_description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Detailed product description'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eco-friendly, premium, business'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'sides_printed': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'double_sided_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'allow_different_designs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_different_designs': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '1'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '0'}),
            'min_order_quantity': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': '1'}),
            'status': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'image_1': forms.FileInput(attrs={'class': 'form-control'}),
            'image_2': forms.FileInput(attrs={'class': 'form-control'}),
            'image_3': forms.FileInput(attrs={'class': 'form-control'}),
            'image_4': forms.FileInput(attrs={'class': 'form-control'}),
            'image_5': forms.FileInput(attrs={'class': 'form-control'}),
            'image_6': forms.FileInput(attrs={'class': 'form-control'}),
        }

