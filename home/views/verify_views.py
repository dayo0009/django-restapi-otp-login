from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View
from django.contrib import messages
from ..auth.verify import VerifyForm
from ..db_functions import get_code


class UserVerification(View):
    @classmethod
    def get(cls, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to continue!!!')
            return HttpResponseRedirect('login')
        login_id = request.session['id']
        form = VerifyForm()
        data = {'user': form,  'login_id': login_id}
        template = 'landing_page/verify_page.html'
        return render(request, template, data)

    @classmethod
    def post(cls, request):
        form = VerifyForm(request.POST)
        if form.is_valid():
            v_code = form.cleaned_data['verify_code']
            verify = get_code(v_code)
            if verify:
                messages.info(request, "Account successfully activated")
                return redirect('login')
            messages.error(request, 'code incorrect')
        empty_form = VerifyForm()
        return render(request, 'landing_page/verify_page.html', {'user': empty_form})
