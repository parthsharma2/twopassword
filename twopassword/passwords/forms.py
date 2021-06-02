from django import forms
from django.core.exceptions import ValidationError
from twopassword.passwords import models


class PasswordForm(forms.ModelForm):
    class Meta:
        model = models.Password
        exclude = ["owner"]


class PasswordVerificationForm(forms.Form):
    password = forms.CharField(
        label="Password", max_length=256, widget=forms.PasswordInput()
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordVerificationForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        if not self.user.check_password(password):
            raise ValidationError("Invalid password")
