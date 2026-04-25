from django.db import models


class SingerTone(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    NEUTRAL = 'NEUTRAL', 'Neutral'
    CHILD = 'CHILD', 'Child'
