import requests
import traceback
import json
import scrapy
import sys

from scrapy.spiders import CrawlSpider
from itertools import cycle
from lxml.html import fromstring
from scraper_api import ScraperAPIClient

from ..load_properties import load_properties


class AHProductIdSpider(scrapy.Spider):
    name = "ah_products"

    def __init__(self):
        super()
        self.properties = load_properties()

    def start_requests(self):
        secret = self.properties.properties['Scraper_secret']
        print("Properties:", self.properties.properties)
        scrape_url = "Scraper_AH_scrape_url"
        client = ScraperAPIClient(secret)

        start_urls = list()
        priorities = list()
        for i in self.properties.properties.keys():
            if str(i).startswith(scrape_url):
                start_urls.append(self.properties.properties[i])
                priorities.append(i.split("_")[4])
        print("Key start urls are:", start_urls, "Priorities:", priorities)
        urls = set()
        for priority, url in zip(priorities, start_urls):
            urls.add(url + '?page=' + str(100))
            print("Calling yield function for url: ", url + '?page=' + str(100))
            yield scrapy.Request(
                client.scrapyGet(url=url + '?page=' + str(100)),
                self.parse, dont_filter=True, priority=int(priority))

    def parse(self, response):
        # print("Inside parse function", response.text)
        rows = response.xpath('//a/@href').extract()
        # print("Rows are:", rows)
        with open("ah_product_ids.json.json", "a") as file:
            for index, product in enumerate(rows):
                if '/producten/product/wi' in product:
                    json.dump({
                        'product_id': product
                    }, file)
                    if index < len(rows) - 1:
                        file.write(',')

