from django.db import models
from django.contrib.auth.models import User


class Password(models.Model):
    """Stores a single password entry."""
    website_name = models.CharField(max_length=64)
    website_address = models.CharField(max_length=253)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
