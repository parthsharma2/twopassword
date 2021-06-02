from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from twopassword.passwords.encryptor import Encryptor
from twopassword.passwords.forms import PasswordForm, PasswordVerificationForm
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

    if request.method == "POST":
        form = PasswordForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.password = encryptor.encrypt(instance.password)
            instance.owner = request.user

            instance.save()

            return render(request, "passwords/add_success.html")
    else:
        form = PasswordForm()

    return render(request, "passwords/add.html", {"form": form})


@login_required
def delete_password(request, password_id):
    """
    Asks for user confirmation & deletes the password entry.

    **Template:**

    :template:`passwords/delete.html`
    :template:`passwords/delete_success.html`
    """
    if request.method == "POST":
        instance = get_object_or_404(models.Password, pk=password_id)

        if instance.owner != request.user:
            return HttpResponseForbidden()

        instance.delete()

        return render(request, "passwords/delete_success.html")
    return render(request, "passwords/delete.html")


@login_required
def show_password(request, password_id):
    """
    Verifies the logged in user's password & shows the decrypted password.

    **Context**

    ``form``
        An instance of :form:`twopassword.passwords.forms.PasswordVerificationForm`.

    **Template:**

    :template:`passwords/show.html`
    :template:`passwords/verification.html`
    """
    encryptor = Encryptor()

    if request.method == "POST":
        form = PasswordVerificationForm(user=request.user, data=request.POST)

        if form.is_valid():
            instance = get_object_or_404(
                models.Password, id=password_id, owner=request.user
            )
            instance.password = encryptor.decrypt(instance.password)

            return render(request, "passwords/show.html", {"obj": instance})

    else:
        form = PasswordVerificationForm(user=request.user)

    return render(request, "passwords/verification.html", {"form": form})


@login_required
def generate_password(request):
    """
    Generates a random 15 character password & returns it as a JSON response.
    """
    password = BaseUserManager().make_random_password(15)
    return JsonResponse({"password": password})


class PasswordListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = "passwords/dashboard.html"

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get("q", "")

        return (
            models.Password.objects.filter(owner=user)
            .filter(
                Q(website_name__icontains=query) | Q(website_address__icontains=query)
            )
            .order_by("website_name")
        )
