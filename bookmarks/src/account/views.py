from django.shortcuts import render
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from shared.mixins import AjaxRequiredMixin
from actions.utils import create_action
from actions.models import Action

from .forms import UserRegistrationForm, UserProfileEditForm
from .models import Contact


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, format=None):
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id', flat=True)
        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions\
            .select_related('user', 'user__profile')\
            .prefetch_related('target')[:10]
        return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('dashboard')


class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = 'account/edit.html'
    success_message = 'Profile Updated Successfuly'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        kwargs.update(instance={
            'user': self.object,
            'profile': self.object.profile,
        })
        return kwargs


class UserListView(LoginRequiredMixin, ListView):
    queryset = User.objects.filter(is_active=True)
    template_name = 'account/user/list.html'
    context_object_name = 'users'
    extra_context = {
        'section': 'people'
    }


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/user/detail.html'
    context_object_name = 'user'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    extra_context = {
        'section': 'people'
    }


class UserFollowView(LoginRequiredMixin, AjaxRequiredMixin, View):
    def post(self, request, format=None):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                if action == 'follow':
                    Contact.objects.get_or_create(
                        user_from=request.user,
                        user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    Contact.objects.filter(user_from=request.user,
                                           user_to=user).delete()
                return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'ko'})
        return JsonResponse({'status': 'ko'})
