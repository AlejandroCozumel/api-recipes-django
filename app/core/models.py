"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from ckeditor.fields import RichTextField


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tours(models.Model):
    """Tours object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = RichTextField()
    time_minutes = models.IntegerField()

    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag to be used for a tour."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PricingOption(models.Model):
    tour = models.ForeignKey(
        'Tours',
        on_delete=models.CASCADE,
        related_name='pricing_options'
    )
    option_name = models.CharField(max_length=255)
    option_price = models.DecimalField(max_digits=8, decimal_places=2)
    special_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    includes = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.option_name} - {self.option_price}"

    def save(self, *args, **kwargs):
        # Calculate and set special_price if discount_percentage is provided
        if self.discount_percentage is not None:
            self.special_price = self.option_price - (
                self.option_price * (self.discount_percentage / 100)
            )

        # Calculate and set discount_percentage if special_price is provided
        elif self.special_price is not None:
            self.discount_percentage = (
                (self.option_price - self.special_price) / self.option_price
            ) * 100

        super().save(*args, **kwargs)


class FavoriteTour(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    tour = models.ForeignKey('Tours', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.tour}"
