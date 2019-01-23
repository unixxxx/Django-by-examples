from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/',
         views.PostListView.as_view(), name='post_list_by_tag'),
    path('<slug:slug>',
         views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/',
         views.PostShareView.as_view(), name='post_share'),
]
