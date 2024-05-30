from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import Form
from .models import Profile


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First Name"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
        error_messages={"exists": "Email already exists"},
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    referred_code = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Referral Code (Optional)"}),
        max_length=6,
        required=False,
    )
    is_active = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').strip()
        if not first_name:
            raise ValidationError('First name cannot be empty')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip()
        if not last_name:
            raise ValidationError('Last name cannot be empty')
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError(self.fields["email"].error_messages["exists"])
        if not email:
            raise ValidationError('Email cannot be empty')
        return self.cleaned_data["email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("phone", "gender", "date_of_birth", "image")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'exists': 'Thsi email already exists.',
        }
    )
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name').strip()
        if not first_name:
            raise ValidationError('First name cannot be empty')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name').strip()
        if not last_name:
            raise ValidationError('Last name cannot be empty')
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if not email:
            raise ValidationError('Email cannot be empty')
        return self.cleaned_data["email"]
