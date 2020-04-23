from django.db import models
from django.utils import timezone
from products.models import BaseProduct


class CoopProduct(BaseProduct):
    product_id = models.BigIntegerField(verbose_name="product id", unique_for_date=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        value = 'product_id: {product_id}'.format(product_id=self.product_id) + ', entry_date:' + str(self.entry_date)
        if self.entry_date is None:
            return value
        else:
            return value + ', entry_date:' + '{:%Y-%m-%d %H:%M}'.format(self.entry_date)

    class Meta:
        ordering = ['entry_date', "-product_id"]
