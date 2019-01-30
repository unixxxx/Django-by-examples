from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views

app_name = 'orders'

urlpatterns = [
    path(_('create/'), views.OrderCreateView.as_view(), name='order_create'),
]
