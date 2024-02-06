from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)

        user.is_admin = True
        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ["email"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
