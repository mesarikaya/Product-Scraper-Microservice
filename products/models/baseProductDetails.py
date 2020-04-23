from django.db import models
from django.utils import timezone


class BaseProductDetails(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    image_url = models.CharField(max_length=250, blank=True)
    price_now = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_now_unit_size = models.CharField(max_length=50, blank=True)
    price_unit_info = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    price_unit_info_unit_size = models.CharField(max_length=50, blank=True)
    catalog_id = models.PositiveIntegerField(verbose_name="item catalog id", null=True, blank=True)
    brand = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)
    hq_id = models.PositiveIntegerField(null=True, blank=True)
    is_medicine = models.BooleanField(null=True, blank=True)
    properties = models.TextField(blank=True)
    entry_date = models.DateTimeField(verbose_name="entry date", null=True, default=timezone.now)

    class Meta:
        abstract = True

