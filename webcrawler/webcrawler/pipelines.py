# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from products.models import AlbertHeijnProduct

class WebcrawlerPipeline(object):
    def process_item(self, item, spider):

        proxy = item['product_id']
        AlbertHeijnProduct.objects.create(product_id=product_id)

        return item
