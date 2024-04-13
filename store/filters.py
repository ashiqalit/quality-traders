import django_filters
from .models import Product, Category, Brand, Sub_category
# class ProductFilter(django_filters.FilterSet):
#     category = django_filters.ModelMultipleChoiceFilter(
#         queryset=Category.objects.all(),
#         label="Category",
#     )
#     brand = django_filters.ModelMultipleChoiceFilter(
#         queryset=Brand.objects.all(),
#         label="Brand",
#     )
#     class Meta:
#         model = Product
#         fields = ['name','category','brand']