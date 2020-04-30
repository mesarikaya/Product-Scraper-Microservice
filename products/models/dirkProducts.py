from django.db import models
from products.models import BaseProduct


class DirkProduct(BaseProduct):
    product_id = models.BigIntegerField(verbose_name="product id", unique_for_date=True)
    product_url = models.CharField(max_length=500, verbose_name="product url", blank=False)
    category = models.CharField(max_length=100, verbose_name="category", blank=True)

    def __str__(self):
        value = 'product_id: {product_id}'.format(product_id=self.product_id) +\
                'product url: {product_url}'.format(product_url=self.product_url) + \
                ', entry_date:' + str(self.entry_date)
        if self.entry_date is None:
            return value
        else:
            return value + ', entry_date:' + '{:%Y-%m-%d %H:%M}'.format(self.entry_date)

    class Meta:
        ordering = ['entry_date', "-product_id"]
