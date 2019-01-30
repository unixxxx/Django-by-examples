from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', TemplateView.as_view(template_name='payment/done.html'), name='done'),
    path('canceled/', TemplateView.as_view(template_name='payment/canceled.html'), name='canceled'),
]
