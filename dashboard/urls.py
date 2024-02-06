from django.urls import path
from dashboard import views

urlpatterns = [
    path ('', views.dashboard, name = 'dashboard'),
    path ('login', views.adminLogin, name = 'dashboard_login'),
    path ('logout', views.logout, name = 'dashboard_logout'),
    # path ('create/', views.create_user, name = 'create_user'),

# users

    path ('users/', views.list_user, name = 'read_user'),
    path('users/update_user_status/', views.update_user_status, name='update_user_status'),

# categories

    path ('categories/', views.list_categories, name = 'read_categories'),
    path ('create_category/', views.create_categories, name = 'create_category'),
    path ('edit_category/<int:pk>/', views.update_category, name = 'edit_category'),
    path ('delete_category/', views.drop_category, name = 'delete_category'),

# products

    path ('products/', views.list_products, name = 'read_products'),
    path ('create_product/', views.create_products, name = 'create_product'),
    path ('edit_product/<str:pk>', views.edit_product, name = 'edit_product'),
    path ('delete_product/', views.drop_product, name = 'delete_product'),

# subcategories
    path ('subcategories/', views.list_subcategories, name = 'read_subcategories'),
    path ('create_subcategory/', views.create_subcategories, name = 'create_subcategory'),
    path ('edit_subcategory/<int:pk>/', views.update_subcategory, name = 'edit_subcategory'),
    path ('delete_subcategory/', views.drop_subcategory, name = 'delete_subcategory'),

# brands
    path ('brands/', views.list_brands, name = 'read_brands'),
    path ('create_brand/', views.create_brands, name = 'create_brand'),
    path ('edit_brand/<int:pk>/', views.update_brand, name = 'edit_brand'),
    path ('delete_brand/', views.drop_brand, name = 'delete_brand'),


    # path ('update/<int:pk>/', views.update_user, name = 'update_user'),
    # path ('delete/<int:pk>/', views.delete_user, name = 'delete_user'),
]