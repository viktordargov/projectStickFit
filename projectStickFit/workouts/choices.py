from django.db import models


class WorkoutTypeChoices(models.TextChoices):
    TOTAL_BODY = "Total Body", "Total Body"
    DYNAMIC_BALANCE = "Dynamic Balance", "Dynamic Balance"
    MUSCLE_FOCUS = "Muscle Focus", "Muscle Focus"

