from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from accounts.forms import SignUpForm, UserProfileUpdateForm
from accounts.models import Profile


class ProfileDetailsView(DetailView):
    template_name = "profile.html"
    model = Profile

class ProfileUpdateView(UpdateView):
    template_name = "forms/form.html"
    form_class = UserProfileUpdateForm
    model = Profile
    success_url = reverse_lazy('index')


class SubmittableLoginView(LoginView):
    template_name = "forms/form.html"

class SignUpView(CreateView):
    template_name = "forms/form.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')

class SubmittablePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "forms/form.html"
    success_url = reverse_lazy('index')