from django import forms

from .models import CustomUser, ShippingAddress





class CustomForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company_name',
            'country'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'country': forms.Select(attrs={
                'class': 'form-control'
            }),
        }




class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'address_1',
            'address_2',
            'city',
            'state',

        ]
        widgets = {
            'address_1': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address_2': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control'
            }),


        }