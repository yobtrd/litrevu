from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model based on Auth's core features."""

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Nom d'utilisateur"
    )
    password = models.CharField(max_length=128)
