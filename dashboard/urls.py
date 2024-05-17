from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login", views.admin_login, name="dashboard_login"),
    path("logout", views.logout, name="dashboard_logout"),
    # path ('create/', views.create_user, name = 'create_user'),
    # users
    path("users/", views.list_user, name="read_user"),
    path(
        "users/update_user_status/", views.update_user_status, name="update_user_status"
    ),
    # categories
    path("categories/", views.list_categories, name="read_categories"),
    path("create_category/", views.create_categories, name="create_category"),
    path("edit_category/<int:pk>/", views.update_category, name="edit_category"),
    path("delete_category/", views.drop_category, name="delete_category"),
    # products
    path("products/", views.list_products, name="read_products"),
    path("create_product/", views.create_products, name="create_product"),
    path("edit_product/<str:pk>", views.edit_product, name="edit_product"),
    path("delete_product/", views.drop_product, name="delete_product"),
    # subcategories
    path("subcategories/", views.list_subcategories, name="read_subcategories"),
    path("create_subcategory/", views.create_subcategories, name="create_subcategory"),
    path(
        "edit_subcategory/<int:pk>/", views.update_subcategory, name="edit_subcategory"
    ),
    path("delete_subcategory/", views.drop_subcategory, name="delete_subcategory"),
    # brands
    path("brands/", views.list_brands, name="read_brands"),
    path("create_brand/", views.create_brands, name="create_brand"),
    path("edit_brand/<int:pk>/", views.update_brand, name="edit_brand"),
    path("delete_brand/", views.drop_brand, name="delete_brand"),
    # path ('update/<int:pk>/', views.update_user, name = 'update_user'),
    # path ('delete/<int:pk>/', views.delete_user, name = 'delete_user'),
    # order
    path("orders/", views.list_orders, name="read_orders"),
    path("edit_order/<int:pk>/", views.edit_order, name="edit_order"),
    # path ('edit_order/<int:pk>/', views.change_order_status, name = 'edit_order'),
    path("cancel_order/", views.cancel_order, name="cancel_order"),
    # path('update_order_status/<int:order_pk>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    # order returns
    path("return_orders/", views.return_requests_list, name="read_return_requests"),
    path(
        "approve_return_request/<int:return_request_id>/",
        views.approve_return_request,
        name="approve_return_request",
    ),
    path(
        "reject_return_request/<int:return_request_id>/",
        views.reject_return_request,
        name="reject_return_request",
    ),
    # reports
    path("salesreport/", views.list_sales, name="read_sales"),
    # Generating pdf sales report
    path(
        "generate_sales_report_pdf/",
        views.DownloadPDF.as_view(),
        name="generate_sales_report_pdf",
    ),
    path(
        "generate_sales_report_excel/",
        views.download_excel,
        name="generate_sales_report_excel",
    ),
    # Coupons
    path("coupons/", views.list_coupons, name="read_coupons"),
    path("create_coupon/", views.create_coupon, name="create_coupon"),
    path("edit_coupon/<int:pk>/", views.update_coupon, name="edit_coupon"),
    path("delete_coupon/", views.drop_coupon, name="delete_coupon"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
