from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, username, password=None):
        if not email:
            raise ValueError("Email is required")
        if not full_name:
            raise ValueError("full name is required")

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, username, password):
        user = self.create_user(
            email=email,
            full_name=full_name,
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=200, unique=True)
    full_name = models.CharField(verbose_name="full name", max_length=200)
    username = models.CharField(max_length=200, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name', 'username']

    objects = MyUserManager()

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
