from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, View

from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        self.tag = None
        tag_slug = self.kwargs.get('tag_slug', None)
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
            return super().get_queryset().filter(tags__in=[self.tag])
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostDetailView(View):
    def get(self, request, slug, format=None):
        post = get_object_or_404(Post, slug=slug, status='published')
        comments = post.comments.filter(active=True)
        comment_form = CommentForm()
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        }
        return render(request, 'blog/post/detail.html', context)

    def post(self, request, slug, format=None):
        post = get_object_or_404(Post, slug=slug, status='published')
        comments = post.comments.filter(active=True)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog:post_detail', slug=slug)
        return render(request, 'blog/post/detail.html', {'post': post,
                                                         'comments': comments,
                                                         'comment_form': comment_form})


class PostShareView(View):
    def get(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id, status='published')
        form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': False})

    def post(self, request, post_id, format=None):
        post = get_object_or_404(Post, id=post_id, status='published')
        form = EmailPostForm(request.POST)
        sent = form.send_mail(request, post)
        return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})
