from django.db import models
from django.utils import timezone


class BaseProduct(models.Model):
    entry_date = models.DateTimeField(verbose_name="entry date", null=True, default=timezone.now)

    class Meta:
        abstract = True
