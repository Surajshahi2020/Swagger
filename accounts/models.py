from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        # user.is_buyer = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField()
    role = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    USERNAME_FIELD = "email"

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
