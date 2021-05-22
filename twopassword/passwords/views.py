from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from twopassword.passwords.encryptor import Encryptor
from twopassword.passwords.forms import PasswordForm
from twopassword.passwords import models


@login_required
def add_password(request):
    """
    Display a form to add a password.

    **Context**

    ``form``
        An instance of :form:`twopassword.passwords.forms.PasswordForm`.

    **Template:**

    :template:`passwords/add.html`
    """
    encryptor = Encryptor()

    if request.method == 'POST':
        form = PasswordForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.password = encryptor.encrypt(instance.password)
            instance.owner = request.user

            instance.save()
    else:
        form = PasswordForm()

    return render(request, 'passwords/add.html', {'form': form})


class PasswordListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'passwords/dashboard.html'

    def get_queryset(self):
        user = self.request.user
        return models.Password.objects.filter(owner=user)
