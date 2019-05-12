from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')


class LogoutView(auth_views.LogoutView):
    template_name = 'accounts/logged_out.html'


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile.html'
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'

