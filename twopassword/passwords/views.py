from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from twopassword.passwords.encryptor import Encryptor
from twopassword.passwords.forms import PasswordForm


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
