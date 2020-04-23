# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

class AlbertHeijnProductItem(scrapy.item):
    product_id = scrapy.Field()

class ProxyItem(scrapy.item):
    proxy = scrapy.Field()
    
