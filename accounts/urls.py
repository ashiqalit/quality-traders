from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", views.registerpage, name="register"),
    path("login", views.loginpage, name="login"),
    path("logout", views.logoutpage, name="logout"),
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="registration/pass_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/pass_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/pass_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/pass_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path("view_profile", views.profile, name="view_profile"),
    path("profile_address", views.profile_address, name="profile_address"),
    path("edit_address/<str:pk>", views.edit_address, name="edit_address"),
    path("remove-address", views.remove_address, name="removeaddress"),
    path("profile_orders", views.profile_orders, name="profile_orders"),
]
