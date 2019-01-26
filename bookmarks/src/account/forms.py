from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from betterforms.multiform import MultiModelForm

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'email']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class UserProfileEditForm(MultiModelForm):
    form_classes = {
        'user': UserEditForm,
        'profile': ProfileEditForm,
    }
