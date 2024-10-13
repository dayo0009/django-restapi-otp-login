from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from .models import Login
from django.http import Http404

#   Login = get_user_model()


class CustomUserAuthBackend(BaseBackend):
    def authenticate(self, request, user=None, **kwargs):
        try:
            user = Login.objects.get(Q(email=user) | Q(phone_number=user))
            return user
        except Login.DoesNotExist:
            return ObjectDoesNotExist

    def get_user(self, user_id):
        try:
            return Login.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return EmptyResultSet
