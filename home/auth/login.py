from rest_framework import serializers
from django.db.models import Q
from ..models import Login
from django.core.exceptions import ObjectDoesNotExist


""" Serializer class for Login form below"""


class LoginFormSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=100,  label='Email / Phone Number', required=True,
        error_messages={'blank': 'Enter Email Address or Phone Number'},
        style={
            'input_type': 'text', 'autofocus': True, 'required': True, 'class': 'form-control',
            'placeholder': 'Email or Phone Number', 'id': 'user',
            },
    )

    @staticmethod
    def validate_name(value):
        if not value:
            message = 'Field must not empty'
            return message
        return value

    @staticmethod
    def check_if_user_exists(user):
        try:
            Login.objects.get(Q(email=user) | Q(phone_number=user))
        except ObjectDoesNotExist:
            message = f"{user} does not exist! Please register"
            return message
        return False
