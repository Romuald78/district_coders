# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms

from district.models.user import UserDC


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    class Meta(forms.ModelForm):
        model = UserDC
        fields = ('username', 'first_name', 'last_name', 'email', 'icon', 'description')
