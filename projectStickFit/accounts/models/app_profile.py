from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date

from projectStickFit.accounts.validators import validate_minimum_age

UserModel = get_user_model()


class AppProfile(models.Model):
    user = models.OneToOneField(
        to=UserModel,
        on_delete=models.CASCADE,
    )

    display_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    use_display_name = models.BooleanField(
        default=False,
    )

    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        validators=[validate_minimum_age],
        null=True,
        blank=True,
    )

    weight = models.FloatField(
        validators=[MaxValueValidator(255.0), MinValueValidator(25.0)],
        null=True,
        blank=True,
    )

    height = models.FloatField(
        null=True,
        blank=True,
    )

    profile_picture = CloudinaryField(
        'profile_picture',
        null=True,
        blank=True,
    )

    def get_display_name(self):
        if self.display_name and self.use_display_name:
            return self.display_name
        elif self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return "Anonymous"

    @property
    def age(self):
        today = date.today()
        # Calculate age based on the date_of_birth
        age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age
