# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from district.models.user import UserDC


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['username'].disabled = True
        self.fields['email'].disabled = True

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        if icon:
            from PIL import Image
            img = Image.open(icon)
            max_width = 500
            max_height = 500
            if img.width > max_width or img.height > max_height:
                raise ValidationError(
                    f"The image is too large ({img.width}x{img.height}px). Maximum dimensions allowed: {max_width}x{max_height}px.")
        return icon

    class Meta(forms.ModelForm):
        model = UserDC
        fields = ('username', 'first_name', 'last_name', 'email', 'icon', 'description')

