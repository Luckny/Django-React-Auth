from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

from uuid import uuid4


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
    is_email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()


class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # one user has one confirmation token
    user = models.ForeignKey(User, on_delete=models.CASCADE)
