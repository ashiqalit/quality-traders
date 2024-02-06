import django_filters
from django.forms import ModelForm
from django.contrib.auth.models import User
from store.models import Category, Product, Sub_category, Brand

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name']

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name']

class SubCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Sub_category
        fields = ['name']

class BrandFilter(django_filters.FilterSet):
    class Meta:
        model = Brand
        fields = ['name']