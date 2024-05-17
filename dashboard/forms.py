from django import forms
from django.forms import ModelForm
from store.models import Category, Product, Sub_category, Brand, Order, Coupon

# from django.contrib.auth.hashers import make_password
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            "category",
            "sub_category",
            "image",
            "name",
            "price",
            "offer",
            "brand",
            "availability",
            "quantity",
        )


class SubCategoryForm(ModelForm):
    class Meta:
        model = Sub_category
        fields = ("name", "category")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ("name", "image", "description")
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ("status",)


class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ("coupon_code", "type", "discount", "valid_from", "valid_to", "active")
        widgets = {
            "valid_from": forms.DateInput(attrs={"type": "date"}),
            "valid_to": forms.DateInput(attrs={"type": "date"}),
        }
