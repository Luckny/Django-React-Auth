from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone
from uuid import uuid4
import secrets


class UserManager(BaseUserManager):
    # override create user function.
    # A user is created with an email and a password
    # **extras: fields like first_name, last_name ...
    def create_user(self, email, password, **extras):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email), **extras
        )  # unsaved user model with normalized email

        user.set_password(password)  # takes care of hashing
        user.save()
        return user

    def create_superuser(self, email, password):
        # create a user
        user = self.create_user(email=email, password=password)

        # add privileges
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


# Creating own user model to enforce login with email
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = UserManager()


class OneTimePassword(models.Model):
    # random unique field of 6 characters
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=6, default=secrets.token_hex(3).upper())
    # related user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # OTP expires after 5 minutes of creation
    expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(minutes=5)
    )
