from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect



def user_login(request):
    """
    Allows a user to login.

    **Context**

    ``form``
        An instance of :form:`django.contrib.auth.forms.AuthenticationForm`.

    **Template:**

    :template:`accounts/login.html`
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user and user.is_active:
                login(request, user)
                request.session['last_login_at'] = datetime.now().timestamp()

                next = request.GET.get('next', '/')

                return redirect(next)
            else:
                return HttpResponseServerError('an error occured while logging in')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})
