from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from store.models import Category, Product, Sub_category, Brand, Order, Coupon, Offer

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
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError('Negative price not allowed')
        return price  
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity < 0:
            raise ValidationError('Negative quantity not allowed')
        return quantity  

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if not name:
            raise ValidationError('Name cannot be empty')
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class SubCategoryForm(ModelForm):
    class Meta:
        model = Sub_category
        fields = ("name", "category", "offer")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name').strip()
        if not name:
            raise ValidationError('Name cannot be empty')
        return name
  
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

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

    # def __init__(self, *args, **kwargs):
    #     super(OrderForm, self).__init__(*args, **kwargs)
    #     # Exclude the 'Cancel' status
    #     self.fields['status'].choices = [
    #         choice for choice in Order.order_status if choice[0] != 6
    #     ]
        
class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ("coupon_code", "type", "discount", "valid_from", "valid_to", "active")
        widgets = {
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
       
    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        # format datetime fields to the right format
        self.fields['valid_from'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['valid_to'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        type = self.cleaned_data.get('type')
        if discount and discount < 0:
            raise ValidationError('Negative discount not allowed')
        if discount and type == 'Percentage' and discount > 100:
            raise ValidationError('Discount percent cannot be greater than 100')
        return discount

    def clean(self):
        cleaned_data = super().clean()
        valid_from = self.cleaned_data.get('valid_from')
        valid_to = self.cleaned_data.get('valid_to')
        today = timezone.now()

        if valid_from and valid_to:
            if valid_from > valid_to:
                raise ValidationError({
                    'valid_from': 'From date cannot be greater than to date',
                    'valid_to': 'To date cannot be less than from date',
                })
            if valid_to < today:
                raise ValidationError({
                    'valid_to':'To date cannot be less than today'
                })
            if valid_from == valid_to:
                raise ValidationError({
                    'valid_to':'Valid From and Valid to cannot be equal',
                    'valid_from':'Valid From and Valid to cannot be equal'
                })

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ("name", "valid_from", "valid_to", "discount", "is_active")
        widgets = {
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        # format datetime fields to the right format
        self.fields['valid_from'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['valid_to'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_name(self):
        name = self.cleaned_data.get("name").strip()
        if not name:
            raise ValidationError("Name cannot be empty")
        return name

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount and discount < 0:
            raise ValidationError('Negative discount not allowed')
        if discount and discount > 100:
            raise ValidationError('Discount not allowed more than 100%')
        return discount

    def clean(self):
        cleaned_data = super().clean()
        valid_from = self.cleaned_data.get('valid_from')
        valid_to = self.cleaned_data.get('valid_to')
        today = timezone.now()

        if valid_from and valid_to:
            if valid_from > valid_to:
                raise ValidationError({
                    'valid_from': 'From date cannot be greater than to date',
                    'valid_to': 'To date cannot be less than from date',
                })
            if valid_to < today:
                raise ValidationError({
                    'valid_to':'To date cannot be less than today'
                })
            if valid_from == valid_to:
                raise ValidationError({
                    'valid_to':'Valid From and Valid to cannot be equal',
                    'valid_from':'Valid From and Valid to cannot be equal'
                })