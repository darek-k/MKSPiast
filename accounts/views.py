from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import RegisterForm


class SignIn(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = 'index'
    success_message = 'Zalogowano pomyślnie'


class Logout(SuccessMessageMixin, LogoutView):
    success_message = 'Wylogowano pomyślnie'


class SignUp(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    success_message = 'Pomyślnie utworzono nowego użytkownika'