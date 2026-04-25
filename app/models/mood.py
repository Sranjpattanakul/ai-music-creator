from django.db import models


class Mood(models.TextChoices):
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    ENERGETIC = 'ENERGETIC', 'Energetic'
    CALM = 'CALM', 'Calm'
    ROMANTIC = 'ROMANTIC', 'Romantic'
    INSPIRATIONAL = 'INSPIRATIONAL', 'Inspirational'
