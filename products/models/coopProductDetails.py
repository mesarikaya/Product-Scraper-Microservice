from django.db import models
from products.models import BaseProductDetails


class CoopProductDetails(BaseProductDetails):
    product_id = models.PositiveIntegerField(verbose_name="product id", unique_for_date=True)

    def __str__(self):
        value = 'product_id: {product_id}, title: {title}, brand: {brand}, category: {category}'.format(
                        product_id=self.product_id,
                        title=self.title,
                        brand = self.brand,
                        category = self.category) + \
                   'price_now: {price_now}, price_now_unit_size: {price_now_unit_size}'.format(
                        price_now=self.price_now,
                        price_now_unit_size=self.price_now_unit_size) + \
                   'entry_date:' + str(self.entry_date)
        if self.entry_date is None:
            return value
        else:
            return value + ', entry_date:' + '{:%Y-%m-%d %H:%M}'.format(self.entry_date)

