from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class RobocupUserManager(UserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
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


class Record(models.Model):
    team_name = models.CharField(max_length=100)
    order = models.CharField(max_length=100)


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    birth_date = models.DateTimeField()
    primary_school = models.BooleanField()
    diet = models.CharField(default="Ziadna", max_length=1000)
    accomodation1 = models.BooleanField(default=True)
    accomodation2 = models.BooleanField(default=True)
    food1 = models.BooleanField(default=True)
    food2 = models.BooleanField(default=True)
    food3 = models.BooleanField(default=True)
    supervisor = models.CharField(max_length=100)


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100, unique=True)
    team_leader = models.IntegerField()
    organization = models.CharField(max_length=100)
    competitors = ArrayField(models.IntegerField())
    categories = ArrayField(models.IntegerField())  # v ktorych kategoriach tim sutazi
    category = models.BooleanField(default=True) # T - ZS, F - SS


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    place = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    registration_open = models.BooleanField(default=False) # F - zatvorena, T - otvorena
    is_active = models.BooleanField(default=False) # ci je to aktualny event
    categories = ArrayField(models.IntegerField())


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    primary_school = models.CharField(default=True) # T - ZS, F - SS





