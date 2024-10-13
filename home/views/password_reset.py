import time
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from ..auth.forget_password import ResetPassword
from ..db_functions import reset_user, get_login_id
from ..views.random_code_gen import generate_verification_code


class ResetPasswordView(View):
    @classmethod
    def get(cls, request):
        template_name = 'forms/forget_password.html'
        form = ResetPassword()
        data = {'user': form}
        return render(request, template_name, data)

    @classmethod
    def post(cls, request):
        form = ResetPassword(request.POST)
        new_code = generate_verification_code()
        if form.is_valid():
            user = form.cleaned_data['user']
            encrypt_password = form.cleaned_data['new_pass2']
            #   process user update
            user = reset_user(user)
            for user_p in user:
                user_p.approved = int(0)
                user_p.verification_code = str(new_code)
                user_p.save()
                #   process password update
                password = get_login_id(user_p.id)
                password.password = make_password(encrypt_password)
                password.save()
                messages.info(request, "password successfully changed!!! ")
                time.sleep(30)
                return redirect('login')
        form = ResetPassword()
        return render(request, "forms/forget_password.html", {'form': form})
