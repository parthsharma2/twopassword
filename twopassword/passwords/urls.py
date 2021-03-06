from django.urls import path
from twopassword.passwords import views

urlpatterns = [
    path('passwords/add', views.add_password, name="add-password"),
    path('passwords/delete/<int:password_id>', views.delete_password, name="delete-password"),
    path('passwords/show/<int:password_id>', views.show_password, name="show-password"),
    path('passwords/generate', views.generate_password, name="generate-password"),
    path('', views.PasswordListView.as_view(), name="dashboard"),
]
