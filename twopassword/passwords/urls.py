from django.urls import path
from twopassword.passwords import views

urlpatterns = [
    path('passwords/add', views.add_password, name="create-password"),
]
