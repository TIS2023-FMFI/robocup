from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class RobocupUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class RobocupUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Unique email
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RobocupUserManager()

    USERNAME_FIELD = "email"  # Use email as the unique identifier
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        "auth.Group", blank=True, related_name="robocupuser_set", related_query_name="robocupuser"  # Add related_name
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="robocupuser_set",  # Add related_name
        related_query_name="robocupuser",
    )

    def __str__(self):
        return self.email
