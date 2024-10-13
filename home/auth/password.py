from rest_framework import serializers


""" Serializer class for password form below"""


class UserPasswordFormSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=100, label='', required=True,
        style={'input_type': 'password', 'autofocus': True, 'class': 'form-control',
               'placeholder': 'Password', 'id': 'password'
               }
    )

    @staticmethod
    def validate_password(value):
        if not value:
            message = 'Password field must not empty'
            return message
        return value
