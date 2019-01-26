from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserRegistrationForm, UserProfileEditForm


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, format=None):
        return render(request, 'account/dashboard.html', {'section': 'dashboard'})


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('dashboard')


class EditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = 'account/edit.html'
    success_message = 'Profile Updated Successfuly'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(EditView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile,
        })
        return kwargs
