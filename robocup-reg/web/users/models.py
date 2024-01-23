from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone


class RobocupUserManager(UserManager):
    # model = get_user_model()
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        print("pswd", password, "mail", email, "etc", extra_fields)

        email = self.normalize_email(email)
        print("norm:", email, "model", self.model)

        user = self.model(email=email, is_staff=extra_fields["is_staff"])
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

    def set_model(self, model):
        self.model = model


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Unique email
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = RobocupUserManager()

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_email_field_name(cls):
        return cls.email

    def get_short_name(self):
        return self.email.split("@")[0]


admin.site.register(User)
