from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
import random
import string


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="ecommerce/profile_pic/default.png", upload_to="ecommerce/profile_pic"
    )
    phone = PhoneNumberField(blank=True)
    Gender = (("Male", "Male"), ("Female", "Female"))
    gender = models.CharField(choices=Gender, null=True, max_length=10)
    referral_code = models.CharField(max_length=6, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        # Generate a unique referral code if empty
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        characters = string.digits + string.ascii_uppercase
        while True:
            code = "".join(random.choice(characters) for i in range(6))
            if not Profile.objects.filter(referral_code=code).exists():
                return code
