from django import forms
from django.core.exceptions import ValidationError
from ..db_functions import *


class ResetPassword(forms.Form):
    user = forms.CharField(max_length=30, label='Email / Phone Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter email or phone number ', 'id': 'user'}))
    new_pass1 = forms.CharField(max_length=30, label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password', 'id': 'pass1'}))
    new_pass2 = forms.CharField(max_length=30, label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm New Password', 'id': 'pass2'}))

    def clean_user(self):
        log_user = self.cleaned_data['user']
        check = get_user(log_user)
        if check is None:
            raise ValidationError(f"{log_user} provided is not registered")
        return log_user

    def clean_new_pass1(self):
        password = self.cleaned_data['new_pass1']
        if not password:
            raise ValidationError("Please enter password")
        return password

    def clean_newp2(self):
        confirm_password = self.cleaned_data['new_pass2']
        password = self.cleaned_data['new_pass1']

        if not confirm_password:
            raise ValidationError("Please re-enter password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Password does not match")
        return confirm_password
