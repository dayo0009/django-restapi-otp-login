from django import forms
from rest_framework import serializers
from ..models.login_otp import LoginOtp
from django.core import exceptions


class VerifyForm(forms.Form):
    verify_code = forms.CharField(label='', max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'text-align: center', 'autocomplete': 'off'}))

    def clean_verify_code(self):
        verify_code = self.cleaned_data['verify_code']
        if not verify_code:
            message = 'Provide OTP sent to your phone to continue!'
            return message
        return verify_code

    @staticmethod
    def verify_otp(otp):
        try:
            LoginOtp.objects.get(otp=otp)
        except exceptions.ObjectDoesNotExist as err:
            return err
        return False


    @staticmethod
    def get_by_login_id(login_id):
        try:
            res = LoginOtp.objects.filter(login_id=login_id).last()
            return res
        except exceptions.ObjectDoesNotExist as err:
            return err
            
    
    @staticmethod
    def get_otp_by_id(otp, int_otp_id):
        try:
            LoginOtp.objects.get(Q(otp=otp) & Q(id=int_otp_id))
        except exceptions.ObjectDoesNotExist as err:
            return err
        return False

