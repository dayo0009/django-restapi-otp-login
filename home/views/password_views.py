import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..auth.password import UserPasswordFormSerializer
from ..db_functions import (get_login_id, get_tables)
from ..new.otp_form import OtpNewFormSerializer
from .otp_views import send_otp_to_phone
from ..permissions.permissions import UserCustomAuthentication



class UserPasswordSerializer(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = UserPasswordFormSerializer
    template_name = 'forms/password.html'
    permission_classes = [UserCustomAuthentication]

    def get(self, request):
        form = self.serializer_class()
        otp_serializer = OtpNewFormSerializer()
        email = request.session['email']
        fetch_table = get_tables(email)
        data = {
            'password': form,
            'db_str': fetch_table,
            'otp_form': otp_serializer
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        login_id = request.session['id']
        psw_serializer = self.serializer_class(data=data)
        otp_serializer = OtpNewFormSerializer(data=data)
        password = data['password']
        if not psw_serializer.is_valid():
            message = psw_serializer.validate_password(psw_serializer.field_name)
            messages.error(request, message)
            return redirect('validate_password')
        elif psw_serializer.is_valid():
            get_id = get_login_id(login_id)
            verify_pass = check_password(password, get_id.password)
            if verify_pass:
                if otp_serializer.is_valid():
                    save_otp = otp_serializer.save(login_id=login_id)
                    if save_otp.id:
                        phone = request.session['phone_number']
                        send_otp = send_otp_to_phone(phone, save_otp.otp)
                        if send_otp:
                        	return redirect('otp_page')
                messages.error(request, f"{otp_serializer.errors}")
                return redirect('validate_password')
            messages.error(request, "Password is incorrect!")
            return redirect('validate_password')
