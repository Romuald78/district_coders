# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db import models

from district.models.user import UserDC


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserDC
        fields = ('username',
                  'password1',
                  'password2',
                  'email',
                  'icon',
                  'first_name',
                  'last_name',
                  'description')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email is None or len(email) == 0:
            self.add_error('email', 'Empty email')

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