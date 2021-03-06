import json
import os

import scrapy

from scraper_api import ScraperAPIClient
from ..load_properties import load_properties


class VomarProductIdSpider(scrapy.Spider):
    name = "vomar_products"

    def __init__(self):
        super()
        self.properties = load_properties()

    def start_requests(self):
        secret = self.properties.properties['Scraper_secret']
        print("Properties:", self.properties.properties)
        scrape_url = "Scraper_Vomar_Scrape_url"
        client = ScraperAPIClient(secret)

        for i in self.properties.properties.keys():
            if str(i).startswith(scrape_url):
                url = self.properties.properties[i]
                property_values = self.properties.properties[i].split(";")
                priority = i.split("_")[4]
                try:
                    category = property_values[1]
                except IndexError as e:
                    category = property_values[0].split("/")[-1].replace("?sort=relevancy+asc", "")

                print("Category:", category)

                print("Calling yield function for url: ", url)
                yield scrapy.Request(
                    client.scrapyGet(url=url),
                    self.parse, dont_filter=True, priority=int(priority), meta={'category': category})

    def parse(self, response):
        rows = response.xpath("//div[contains(@class,'productContainer')]//a/@href").extract()
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(fileDir, "webcrawler\\resources\\data\\vomar_product_ids.json")
        with open(file_name, "a") as file:
            for index, product in enumerate(rows):
                print("Product:", product)
                json.dump({
                    'product_id': product,
                    'category': response.meta['category']
                }, file)
                if index < len(rows) - 1:
                    file.write(',')
