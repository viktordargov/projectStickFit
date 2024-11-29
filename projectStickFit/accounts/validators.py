from django.core.exceptions import ValidationError
from datetime import date


def validate_minimum_age(value, min_age=14):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if age < min_age:
        raise ValidationError(f"You must be at least {min_age} years old.")
