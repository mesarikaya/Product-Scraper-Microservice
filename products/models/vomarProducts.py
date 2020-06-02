from django.db import models
from products.models import BaseProduct


class VomarProduct(BaseProduct):
    product_id = models.CharField(max_length=255, verbose_name="product id", unique_for_date=True)
    category = models.CharField(max_length=200, verbose_name="category", blank=True)

    def __str__(self):
        value = 'product_id: {product_id}'.format(product_id=self.product_id) +\
                'product category: {category}'.format(category=self.category) + \
                ', entry_date:' + str(self.entry_date)
        if self.entry_date is None:
            return value
        else:
            return value + ', entry_date:' + '{:%Y-%m-%d %H:%M}'.format(self.entry_date)

    class Meta:
        ordering = ['entry_date', "-product_id"]
