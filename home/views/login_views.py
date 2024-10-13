from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from ..auth.login import LoginForm, LoginFormSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework import status


class UserLogin(View):
    @classmethod
    def get(cls, reqeust):
        template = 'forms/login.html'
        form = LoginForm()
        data = {'user': form}
        return render(reqeust, template, data)

    @classmethod
    def post(cls, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['name']
            db_result = authenticate(request, user=user)
            if db_result is None:
                messages.error(request, f"{user} does not exist! Please register")
            elif db_result is not None:
                new_id = db_result.id
                email = db_result.email
                phone = db_result.phone_number
                approved = db_result.approved
                if approved == '0':
                    request.session['id'] = new_id
                    messages.add_message(request, messages.INFO, f"{user} not verified")
                    login(request, db_result)
                    return redirect('verify_page')
                elif email or phone == user and approved == '1':
                    #   new_id = db_result.id
                    request.session['id'] = new_id
                    request.session['email'] = email
                    request.session['phone_number'] = phone
                    login(request, db_result)
                    return redirect('validate_password')
            form = LoginForm()
        return render(request, 'forms/login.html', {'user': form})


class UserLoginSerializer(APIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    serializer_class = LoginFormSerializer
    template_name = 'forms/login.html'
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    #   @staticmethod
    def get(self, request):
        form = self.serializer_class()
        data = {'user': form}
        return Response(data, status=status.HTTP_200_OK)

    #   @staticmethod
    def post(self, request):
        data = request.data
        serialize_form = self.serializer_class(data=data)
        user = data['name']
        if not serialize_form.is_valid():
            form = self.serializer_class
            message = form.validate_name(serialize_form.field_name)
            messages.error(request, message)
            return redirect('login')
        elif serialize_form.is_valid(raise_exception=True):
            new_user = serialize_form.check_if_user_exists(user)
            if new_user:
                messages.info(request, new_user)
                return redirect('login')
            elif user:
                db_result = authenticate(request, user=user)
                new_id = db_result.id
                email = db_result.email
                phone = db_result.phone_number
                approved = db_result.approved
                if approved == '0':
                    request.session['id'] = new_id
                    messages.add_message(request, messages.INFO, f"{user} not verified")
                    login(request, db_result)
                    return redirect('verify_page')
                elif email or phone == user and approved == '1':
                    request.session['id'] = new_id
                    request.session['email'] = email
                    request.session['phone_number'] = phone
                    login(request, db_result)
                    return redirect('validate_password')
