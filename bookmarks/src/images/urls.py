from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.ImageCreateView.as_view(), name='create'),
    path('detail/<int:id>/<slug:slug>/',
         views.ImageDetailView.as_view(), name='detail'),
    path('like/', views.ImageLikeView.as_view(), name='like'),
    path('', views.ImageListView.as_view(), name='list'),
]
