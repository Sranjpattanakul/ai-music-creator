from django.db import models
from .mood import Mood
from .occasion import Occasion
from .singer_tone import SingerTone


class Prompt(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    occasion = models.CharField(max_length=20, choices=Occasion.choices)
    mood = models.CharField(max_length=20, choices=Mood.choices)
    singer_tone = models.CharField(max_length=20, choices=SingerTone.choices)
    requested_duration = models.CharField(max_length=10, blank=True, default='3:00')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'prompt'

    def __str__(self):
        return self.title
