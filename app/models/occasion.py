from django.db import models


class Occasion(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'Birthday'
    WEDDING = 'WEDDING', 'Wedding'
    ANNIVERSARY = 'ANNIVERSARY', 'Anniversary'
    GRADUATION = 'GRADUATION', 'Graduation'
    CELEBRATION = 'CELEBRATION', 'Celebration'
    CUSTOM = 'CUSTOM', 'Custom'
