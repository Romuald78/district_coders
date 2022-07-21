# authentication/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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