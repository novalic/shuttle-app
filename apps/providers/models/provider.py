from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    # ISO 4217
    currency = models.CharField(
        max_length=3,
        blank=False,
        null=False
    )
    email = models.EmailField(
        blank=False,
        null=False
    )
    # ISO 639-3
    language = models.CharField(
        max_length=2,
        blank=False,
        null=False
    )
    name = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )
    phone_number = PhoneNumberField(
        blank=False,
        null=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
