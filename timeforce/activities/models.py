from django.db import models
from django.contrib.auth.models import User


from timeforce.models import UUIDModel, TimeStampedModel


class Activity(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=128)
    duration = models.PositiveIntegerField(default=0)  # Stored in minutes
    owner = models.ForeignKey(User, related_name="activities", on_delete=models.CASCADE)
    # Add chart foreign key later.

    class Meta:
        verbose_name_plural = "Activities"


# Goal Model
