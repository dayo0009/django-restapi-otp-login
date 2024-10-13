from django.db.models import Q
from django.core import exceptions
from .models import *


def get_user(user):
    try:
        db_user = Login.objects.get(Q(email=user) | Q(phone_number=user))
        if db_user:
            return db_user
    except exceptions.ObjectDoesNotExist:
        return None


def check_email_exist(email):
    try:
        result = Login.objects.filter(email=email).exists()
        return result
    except exceptions.ObjectDoesNotExist:
        return False


def check_phone(phone):
    try:
        result = Login.objects.filter(phone_number=phone).exists()
        return result
    except exceptions.ObjectDoesNotExist:
        return False


def get_login_id(login_id):
    try:
        result = Password.objects.get(login_id=login_id)
        return result
    except exceptions.EmptyResultSet:
        return False

    

def get_otp_by_login_id(login_id):
    try:
        res = LoginOtp.objects.get(login_id=login_id).last()
        return res
    except exceptions.ObjectDoesNotExist:
        return False
