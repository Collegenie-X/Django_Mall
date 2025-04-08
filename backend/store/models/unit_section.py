from django.db import models
from .base import SUBJECT_CHOICES


class UnitType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default="")
    subject = models.CharField(
        max_length=50,
        help_text="* required",
        choices=SUBJECT_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}__({self.subject})"


class SectionType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, default="")
    subject = models.CharField(
        max_length=50,
        help_text="* required",
        choices=SUBJECT_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}__({self.subject})"
