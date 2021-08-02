from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView


# Create your views here.
class AccountView(TemplateView):
    template_name = 'users/account.html'


class SignUpView(TemplateView):
    template_name = 'users/sign_up.html'


class SignInView(TemplateView):
    template_name = 'users/sign_in.html'


def sign_out(request):
    logout(request)
    return redirect(reverse('users:sign-in'))


class ForgottenPasswordView(TemplateView):
    template_name = 'users/forgotten_password.html'


def email(request):
    context = {}
    return render(request, 'users/email.html', context)


def verification(request, uidb64, token):
    context = {}
    return render(request, 'users/verification.html', context)
