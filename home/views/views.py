from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.core import exceptions
from django.contrib import messages
from ..db_functions import phone_accessories, clothing, get_clothing_products
from ..db_functions import get_phone_accessories_products as get_phone
from ..models.login_otp import LoginOtp



# User may want to logout if they forget their password
def sign_out(request):
    #   del request.session['id']
    logout(request)
    messages.info(request, f"You're successfully logged out")
    return redirect('login')


# This code ensure session timeout after five minutes of inactivity
def middleware_logout(request, **kwargs):
    #   del request.session['id']
    logout(request)
    messages.info(request, "session timeout")
    return redirect('login')


# This ensure your online status is disabled when logout
def disable_is_active_if_user_logout(request):
    login_id = request.session['id']
    try:
        res = LoginOtp.objects.filter(login_id=login_id).last()
        res.is_active = 0
        res.save()
        logout(request)
        messages.info(request, "You've successfully logged out")
        return redirect('login')
    except exceptions.ObjectDoesNotExist as err:
        return err
