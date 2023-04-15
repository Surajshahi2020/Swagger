from django.db import models
from django.contrib.auth.hashers import check_password


class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField()
    role = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=True)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
