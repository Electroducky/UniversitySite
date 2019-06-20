from django.shortcuts import render, redirect
from django.views import View

from university_system.auth import auth_user_manager
from university_system.models import user_manager
from university_system.forms.user_forms import *


class Login(View):
    def get(self, request):
        form = LoginForm
        return render(request, "university_system/auth.html", context={"form": form})

    def post(self, request):
        filled_form = LoginForm(request.POST)
        if filled_form.is_valid():
            check = user_manager.check(filled_form.cleaned_data['login'],
                                       filled_form.cleaned_data['password'], True)
            if check is None:
                auth_user = auth_user_manager.log_in(filled_form.cleaned_data['login'])
                request.session['token'] = auth_user.token
                return redirect('home')
            else:
                return render(request, "university_system/auth.html", context={"form": filled_form, 'check': check})
        return redirect('login')


def logout(request):
    if request.session.get('token', None) is not None:
        auth_user_manager.log_out(request.session["token"])
        del request.session['token']
        return redirect('login')