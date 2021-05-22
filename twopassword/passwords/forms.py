from django.forms import ModelForm
from twopassword.passwords import models


class PasswordForm(ModelForm):
    class Meta:
        model = models.Password
        exclude = ['owner']