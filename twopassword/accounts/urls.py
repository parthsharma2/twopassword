from django.contrib.auth.views import LogoutView
from django.urls import path
from twopassword.accounts import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.user_registration, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('logged-out/', views.logged_out, name="logged-out"),
]
