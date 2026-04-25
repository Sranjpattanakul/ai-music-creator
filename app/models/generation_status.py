from django.db import models


class GenerationStatus(models.TextChoices):
    QUEUED = 'QUEUED', 'Queued'
    GENERATING = 'GENERATING', 'Generating'
    SUCCESS = 'SUCCESS', 'Success'
    FAILED = 'FAILED', 'Failed'
