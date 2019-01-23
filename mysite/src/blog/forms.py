from django import forms
from django.core.mail import send_mail
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.TextInput)

    def send_mail(self, request, post):
        if self.is_valid():
            cd = self.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            return True
        return False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
