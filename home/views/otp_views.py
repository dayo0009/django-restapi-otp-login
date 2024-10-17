from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from twilio.rest import Client as TwilioClient
from decouple import config
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View
from ..auth.verify import OtpVerifySerializer, VerifyForm
from ..db_functions import (get_man_table_with_contain_email, get_retail_table_with_contain_email,
                            get_single_table_with_contain_email
                            )
from ..permissions.permissions import UserCustomAuthentication
from ..models.login_otp import LoginOtp


account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_phone = config('TWILIO_PHONE')
client = TwilioClient(account_sid, auth_token)


def send_otp_to_phone(phone, otp):
    message = client.messages.create(
        body="Your Badiiu one time verification code is " + otp,
        from_=twilio_phone,
        to=phone,
    )
    return message.body


class OTPVerification(View):
    @classmethod
    def get(cls, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue!!!')
            return HttpResponseRedirect('login')
        form = VerifyForm()
        login_id = request.session['id']
        query = form.get_by_login_id(login_id)
        data = {'otp': form, 'query': query}
        template = 'landing_page/verify_otp.html'
        return render(request, template, data)

    @classmethod
    def post(cls, request):
        data = request.POST
        form = VerifyForm(data)
        otp = data.get('verify_code')
        login_id = request.session['id']
        if form.is_valid():
            check = form.verify_otp(otp)
            if check:
                res = form.get_by_login_id(login_id)
                res.otp_max_try = int(res.otp_max_try) - 1
                res.save()
                if res.otp_max_try == 2 or res.otp_max_try == 1:
                    messages.error(request,f'Invalid code! {res.otp_max_try} attempt remaining')
                    return redirect('otp_page')
                elif res.otp_max_try <= 0:
                    logout(request)
                    messages.info(request, f"Maximum attempt exceeded!!!")
                    return redirect('login')
                elif otp:
                    invalid_otp_or_id = form.get_otp_by_id(otp, int_otp_id)
                    if invalid_otp_or_id:
                    	messages.error(request, "code already been used or expired")
                    	return redirect('otp_page')
            	    else:
                    	email = request.session['email']
                    	query = LoginOtp.objects.get(Q(otp=otp) & Q(id=int_otp_id))
                    	if query:
                    		query.is_active = 1
                    		query.otp_max_try = int(query.otp_max_try) - 1
                    		query.save()
                    		man_table_name = get_man_table_with_contain_email(email)
                    		single_table_name = get_single_table_with_contain_email(email)
                    		fetch_table_name = get_retail_table_with_contain_email(email)
                    		if fetch_table_name:
                        		return redirect('retailer-dashboard')
                    		elif man_table_name:
                        		return redirect('manufacturer-dashboard')
                    		elif single_table_name:
                        		return redirect('user-dashboard')

