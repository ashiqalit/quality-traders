from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Profile

admin.site.register(Profile)
=======
from accounts.models import Profile
# Register your models here.

# class PhoneInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = "userprofile"

# class UserAdmin(BaseUserAdmin):
#     inlines = [PhoneInline]

# admin.site.unregister(User)
admin.site.register(Profile)
>>>>>>> origin/twilio
