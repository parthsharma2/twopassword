from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
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

def delete_password(request, password_id):
    """
    Asks for user confirmation & deletes the password entry.

    **Template:**

    :template:`passwords/delete.html`
    :template:`passwords/delete_success.html`
    """
    if request.method == 'POST':
        instance = get_object_or_404(models.Password, pk=password_id)

        if instance.owner != request.user:
            return HttpResponseForbidden()

        instance.delete()

        return render(request, 'passwords/delete_success.html')
    else:
        return render(request, 'passwords/delete.html')


class PasswordListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'passwords/dashboard.html'

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get('q', '')

        return models.Password.objects.filter(
            owner=user
        ).filter(
            Q(website_name__icontains=query) | Q(website_address__icontains=query)
        ).order_by('website_name')
