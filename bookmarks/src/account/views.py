from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, format=None):
        return render(request, 'account/dashboard.html', {'section': 'dashboard'})
