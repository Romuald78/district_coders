# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms

from district.models.user import UserDC


class UserUpdateForm(forms.ModelForm):

    class Meta(forms.ModelForm):
        model = UserDC
        fields = ('first_name', 'last_name', 'icon', 'description')
