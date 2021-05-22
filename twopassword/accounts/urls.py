from django.urls import path
from twopassword.accounts import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.user_registration, name="register"),
]
