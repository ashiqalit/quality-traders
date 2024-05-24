from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import Address


class AddressForm(forms.ModelForm):
    fname = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Firstname", "style": "width: 200px;"}
        ),
        label="First Name",
    )
    lname = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Lastname", "style": "width: 200px;"}
        ),
        label="Last Name",
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Email", "style": "width: 200px;"}
        )
    )
    phone = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Phone Number", "style": "width: 200px;"}
        )
    )
    pincode = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Pincode", "style": "width: 200px;"}
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter Address", "style": "width: 200px;"}
        )
    )

    class Meta:
        model = Address
        fields = ("fname", "lname", "email", "phone", "pincode", "address")
    
    def clean_fname(self):
        fname = self.cleaned_data.get('fname').strip()
        if not fname:
            raise ValidationError('First name cannot be empty')
        return fname
    
    def clean_lname(self):
        lname = self.cleaned_data.get('lname').strip()
        if not lname:
            raise ValidationError('Last name cannot be empty')
        return lname
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if not email:
            raise ValidationError('Email cannot be empty')
        return self.cleaned_data["email"]
  
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode').strip()
        if not pincode:
            raise ValidationError('Pincode cannot be empty')
        return self.cleaned_data["pincode"]
  
    def clean_address(self):
        address = self.cleaned_data.get('address').strip()
        if not address:
            raise ValidationError('Address cannot be empty')
        return self.cleaned_data["address"]