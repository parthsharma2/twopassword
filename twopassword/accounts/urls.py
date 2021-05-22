from django.urls import path
from twopassword.accounts import views

urlpatterns = [
    path('login/', views.user_login, name="login"),
]
