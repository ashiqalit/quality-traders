from django import forms
from django.forms import ModelForm
from store.models import Category,Product,Sub_category,Brand,Order
# from django.contrib.auth.hashers import make_password

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }   

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('category','sub_category','image','name','price','brand','availability','quantity')

class SubCategoryForm(ModelForm):
    class Meta:
        model = Sub_category
        fields = ('name','category')
        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control'}),

        }   

class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ('name','image','description')
        widgets = {

            'description': forms.TextInput(attrs={'class': 'form-control'}),

        }   

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
          